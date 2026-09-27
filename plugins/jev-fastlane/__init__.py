"""Jev Fastlane — low-latency decision routing and mutation guardrails for Hermes.

The plugin deliberately uses Jev only where its System One shape is useful:

* one batched route decision before the main LLM turn;
* one extra decision only before genuinely high-risk/mutating tool calls;
* no Jev call for ordinary read-only tool calls or post-response prose rewriting.

It never sends secrets verbatim: likely credentials are redacted before any TypeSafe request.
Routing failures fail open to the existing Hermes runtime; deterministic catastrophic shell
patterns still fail closed. This preserves availability while adding a cheap decision layer.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_VERSION = "1.0.0"
_DEFAULT_BASE_URL = "https://api.typesafe.ai"
_DEFAULT_MODEL = "jev-latest"

_SECRET_KEY_RE = re.compile(
    r"(?:password|passwd|secret|token|api[_-]?key|authorization|cookie|credential|application[_-]?password)",
    re.IGNORECASE,
)
_SECRET_TEXT_PATTERNS = (
    re.compile(r"(?i)\b(Bearer\s+)[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"(?i)\b(password|passwd|secret|token|api[_-]?key|application[_-]?password)\s*[:=]\s*[^\s,;]+"
    ),
)

_CATASTROPHIC_TERMINAL_RE = re.compile(
    r"(?ix)(?:"
    r"\brm\s+-[^\n\r]*r[^\n\r]*\s+/(?:\s|$)|"
    r"\brm\s+-[^\n\r]*r[^\n\r]*\s+/\*|"
    r"\bmkfs(?:\.[a-z0-9]+)?\s+/dev/|"
    r"\bdd\s+[^\n\r]*\bof=/dev/(?:sd|nvme|vd|xvd)|"
    r":\(\)\s*\{\s*:\|:&\s*;\s*\}:"
    r")"
)

_MUTATING_TERMINAL_RE = re.compile(
    r"(?ix)(?:"
    r"\bgit\s+(?:push|merge|rebase|reset\s+--hard|clean\s+-[a-z]*f)|"
    r"\bwp\s+[^\n\r]*(?:\bupdate\b|\bdelete\b|\bcreate\b|\binstall\b|\bactivate\b|\bdeactivate\b)|"
    r"\bcurl\b[^\n\r]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE)\b|"
    r"\bsystemctl\s+(?:restart|stop|disable|enable|mask)\b|"
    r"\bservice\s+\S+\s+(?:restart|stop)\b|"
    r"\bdocker\s+(?:rm|rmi|stop|restart|system\s+prune)\b|"
    r"\bdocker\s+compose\s+(?:up|down|restart)\b|"
    r"\bkubectl\s+(?:apply|delete|patch|replace|rollout|set)\b|"
    r"\bterraform\s+(?:apply|destroy)\b|"
    r"\bansible-playbook\b|"
    r"\bcrontab\s+(?:-[er]|\S+)|"
    r"\bshutdown\b|\breboot\b"
    r")"
)

_EXTERNAL_MUTATION_TOOL_RE = re.compile(
    r"(?i)(?:wordpress|github|gmail|email|slack|calendar|stripe|cloudflare|vercel|supabase|database|sql|webhook|deploy|publish)"
    r".*(?:create|update|delete|remove|send|publish|deploy|merge|push|write|execute|cancel|archive|trash)"
    r"|(?:create|update|delete|remove|send|publish|deploy|merge|push|cancel|archive|trash)"
    r".*(?:wordpress|github|gmail|email|slack|calendar|stripe|cloudflare|vercel|supabase|database|sql|webhook)",
)


@dataclass(frozen=True)
class _RouteDecision:
    intent: str
    intent_confidence: float
    requires_tools: float
    requires_current_data: float
    mutation_intent: float
    needs_deep_reasoning: float
    needs_post_action_verification: float
    risk_score: float
    response_length: str
    resolved_model: str
    latency_ms: int
    input_tokens: int


class _FastlaneRuntime:
    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.runtime_enabled = True
        self.client: httpx.Client | None = None
        self.client_identity: tuple[str, str] | None = None
        self.cache: OrderedDict[str, tuple[float, dict[str, Any]]] = OrderedDict()
        self.routes_by_session: dict[str, tuple[_RouteDecision, str]] = {}
        self.failures_in_row = 0
        self.circuit_open_until = 0.0
        self.calls = 0
        self.cache_hits = 0
        self.failures = 0
        self.total_latency_ms = 0
        self.total_input_tokens = 0
        self.last_error = ""
        self.last_model = ""


_runtime = _FastlaneRuntime()


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float, *, minimum: float, maximum: float) -> float:
    try:
        value = float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return min(maximum, max(minimum, value))


def _env_int(name: str, default: int, *, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return min(maximum, max(minimum, value))


def _configured() -> bool:
    return bool(os.getenv("TYPESAFE_API_KEY", "").strip())


def _enabled() -> bool:
    return _runtime.runtime_enabled and _env_bool("JEV_FASTLANE_ENABLED", True) and _configured()


def _redact_text(text: str) -> str:
    redacted = text
    for pattern in _SECRET_TEXT_PATTERNS:
        if pattern.pattern.startswith(r"(?i)\b(Bearer"):
            redacted = pattern.sub(r"\1[REDACTED]", redacted)
        elif "password|passwd" in pattern.pattern:
            redacted = pattern.sub(lambda m: f"{m.group(1)}=[REDACTED]", redacted)
        else:
            redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def _sanitize_value(value: Any, *, depth: int = 0) -> Any:
    if depth >= 6:
        return "[TRUNCATED]"
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for index, (key, item) in enumerate(value.items()):
            if index >= 40:
                result["__truncated__"] = True
                break
            key_text = str(key)
            if _SECRET_KEY_RE.search(key_text):
                result[key_text] = "[REDACTED]"
            else:
                result[key_text] = _sanitize_value(item, depth=depth + 1)
        return result
    if isinstance(value, (list, tuple)):
        items = list(value)[:30]
        sanitized = [_sanitize_value(item, depth=depth + 1) for item in items]
        if len(value) > len(items):
            sanitized.append("[TRUNCATED]")
        return sanitized
    if isinstance(value, str):
        return _redact_text(value[:12000])
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return _redact_text(str(value)[:2000])


def _get_client() -> httpx.Client:
    key = os.getenv("TYPESAFE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("TYPESAFE_API_KEY is not configured")
    base_url = os.getenv("TYPESAFE_BASE_URL", _DEFAULT_BASE_URL).strip().rstrip("/") or _DEFAULT_BASE_URL
    identity = (hashlib.sha256(key.encode("utf-8")).hexdigest()[:12], base_url)
    with _runtime.lock:
        if _runtime.client is not None and _runtime.client_identity == identity:
            return _runtime.client
        if _runtime.client is not None:
            try:
                _runtime.client.close()
            except Exception:
                pass
        timeout_ms = _env_int("JEV_FASTLANE_TIMEOUT_MS", 450, minimum=100, maximum=5000)
        timeout_s = timeout_ms / 1000.0
        _runtime.client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {key}",
                "Accept": "application/json",
                "User-Agent": f"hermes-jev-fastlane/{_VERSION}",
            },
            timeout=httpx.Timeout(timeout_s, connect=min(0.25, timeout_s)),
            limits=httpx.Limits(max_connections=8, max_keepalive_connections=4, keepalive_expiry=30.0),
        )
        _runtime.client_identity = identity
        return _runtime.client


def _cache_key(state: Any, questions: dict[str, Any], model: str) -> str:
    raw = json.dumps(
        {"state": state, "questions": questions, "model": model},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _call_jev(
    *,
    state: Any,
    questions: dict[str, Any],
    cacheable: bool,
) -> dict[str, Any] | None:
    if not _enabled():
        return None

    now = time.monotonic()
    with _runtime.lock:
        if _runtime.circuit_open_until > now:
            return None

    model = os.getenv("JEV_FASTLANE_MODEL", os.getenv("TYPESAFE_DEFAULT_MODEL", _DEFAULT_MODEL)).strip() or _DEFAULT_MODEL
    key = _cache_key(state, questions, model)
    if cacheable:
        ttl = _env_int("JEV_FASTLANE_CACHE_TTL_SECONDS", 300, minimum=0, maximum=3600)
        with _runtime.lock:
            entry = _runtime.cache.get(key)
            if entry is not None and entry[0] >= now:
                _runtime.cache.move_to_end(key)
                _runtime.cache_hits += 1
                return entry[1]
            if entry is not None:
                _runtime.cache.pop(key, None)

    payload = {"state": state, "model": model, "questions": questions}
    started = time.perf_counter()
    try:
        response = _get_client().post("/v1/systemone", json=payload)
        response.raise_for_status()
        body = response.json()
        if not isinstance(body, dict) or not isinstance(body.get("answers"), dict):
            raise ValueError("TypeSafe response did not contain an answers object")
    except Exception as exc:
        with _runtime.lock:
            _runtime.failures += 1
            _runtime.failures_in_row += 1
            _runtime.last_error = f"{type(exc).__name__}: {str(exc)[:180]}"
            threshold = _env_int("JEV_FASTLANE_CIRCUIT_FAILURES", 3, minimum=1, maximum=20)
            if _runtime.failures_in_row >= threshold:
                cooldown = _env_int("JEV_FASTLANE_CIRCUIT_SECONDS", 60, minimum=5, maximum=900)
                _runtime.circuit_open_until = time.monotonic() + cooldown
        logger.debug("Jev fastlane bypass after request failure: %s", type(exc).__name__)
        return None

    latency_ms = int(round((time.perf_counter() - started) * 1000))
    usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
    input_tokens = usage.get("input_tokens", 0)
    try:
        input_tokens_int = max(0, int(input_tokens or 0))
    except (TypeError, ValueError):
        input_tokens_int = 0

    with _runtime.lock:
        _runtime.calls += 1
        _runtime.failures_in_row = 0
        _runtime.circuit_open_until = 0.0
        _runtime.total_latency_ms += latency_ms
        _runtime.total_input_tokens += input_tokens_int
        _runtime.last_error = ""
        _runtime.last_model = str(body.get("model") or model)
        if cacheable:
            ttl = _env_int("JEV_FASTLANE_CACHE_TTL_SECONDS", 300, minimum=0, maximum=3600)
            if ttl > 0:
                _runtime.cache[key] = (time.monotonic() + ttl, body)
                _runtime.cache.move_to_end(key)
                cache_max = _env_int("JEV_FASTLANE_CACHE_MAX", 256, minimum=8, maximum=4096)
                while len(_runtime.cache) > cache_max:
                    _runtime.cache.popitem(last=False)

    body["_fastlane_latency_ms"] = latency_ms
    body["_fastlane_input_tokens"] = input_tokens_int
    return body


def _choice(answers: dict[str, Any], name: str, default: str = "other") -> tuple[str, float]:
    raw = answers.get(name)
    if not isinstance(raw, dict) or raw.get("type") != "choice":
        return default, 0.0
    choice = str(raw.get("choice") or default)
    confidence_raw = raw.get("confidence", 0.0)
    try:
        confidence = float(confidence_raw or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0
    return choice, min(1.0, max(0.0, confidence))


def _noul(answers: dict[str, Any], name: str) -> float:
    raw = answers.get(name)
    if not isinstance(raw, dict) or raw.get("type") != "noul":
        return 0.5
    try:
        return min(1.0, max(0.0, float(raw.get("noul", 0.5))))
    except (TypeError, ValueError):
        return 0.5


def _score(answers: dict[str, Any], name: str) -> float:
    raw = answers.get(name)
    if not isinstance(raw, dict) or raw.get("type") != "score":
        return 1.5
    try:
        return min(3.0, max(0.0, float(raw.get("score", 1.5))))
    except (TypeError, ValueError):
        return 1.5


def _recent_context(history: Any, current_message: str) -> list[dict[str, str]]:
    if not isinstance(history, list):
        return []
    result: list[dict[str, str]] = []
    skipped_current = False
    for item in reversed(history):
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "")
        if role not in {"user", "assistant"}:
            continue
        content = item.get("content")
        if not isinstance(content, str) or not content.strip():
            continue
        cleaned = _redact_text(content.strip())
        if role == "user" and not skipped_current and cleaned == _redact_text(current_message.strip()):
            skipped_current = True
            continue
        result.append({"role": role, "text": cleaned[:600]})
        if len(result) >= 2:
            break
    result.reverse()
    return result


def _route_questions() -> dict[str, Any]:
    return {
        "intent": {
            "type": "choice",
            "instructions": "Classify the user's immediate task by the work the main agent should perform next.",
            "criteria": {
                "direct_answer": "Answer from stable knowledge without external tools.",
                "current_research": "Needs current web/external evidence or live state.",
                "coding": "Inspect, change, test, or reason about software/code.",
                "wordpress_read": "Inspect a WordPress site without changing it.",
                "wordpress_write": "Modify WordPress content/configuration/state.",
                "repo_ops": "Inspect or modify a Git repository/GitHub state.",
                "automation_ops": "Operate or troubleshoot bots, servers, schedules, agents, or automation.",
                "file_analysis": "Read or analyze user/project files.",
                "other": "None of the other categories clearly fits.",
            },
        },
        "requires_tools": {
            "type": "noul",
            "instructions": "Does completing this request correctly require using at least one external/tool call rather than only answering in text?",
        },
        "requires_current_data": {
            "type": "noul",
            "instructions": "Would stale model knowledge materially risk an incorrect answer, so current external data should be checked?",
        },
        "mutation_intent": {
            "type": "noul",
            "instructions": "Is the user explicitly asking the agent to change, send, publish, delete, deploy, execute, or otherwise mutate external or persistent state now?",
        },
        "needs_deep_reasoning": {
            "type": "noul",
            "instructions": "Does this task genuinely need deep multi-step reasoning rather than a bounded direct solution?",
        },
        "needs_post_action_verification": {
            "type": "noul",
            "instructions": "If tools perform an action, should the agent verify resulting state before claiming success?",
        },
        "risk": {
            "type": "score",
            "instructions": "Rate execution risk if the agent follows the request. Consider irreversibility, production impact, secrets, money, publication, deletion, deployment, and account changes.",
            "criteria": [
                "Low: read-only or easily reversible local work.",
                "Moderate: bounded reversible changes with clear targets.",
                "High: production/external writes, publishing, sending, deployments, credentials, or broad changes.",
                "Critical: destructive/irreversible operations, security-sensitive actions, money movement, or unclear high-impact targets.",
            ],
        },
        "response_length": {
            "type": "choice",
            "instructions": "Choose the shortest response length that can fully satisfy the user's immediate request.",
            "criteria": {
                "brief": "A few direct sentences or commands are enough.",
                "normal": "A compact explanation plus the necessary implementation details.",
                "detailed": "The task needs substantial technical detail, evidence, or a multi-step deliverable.",
            },
        },
    }


def _route_decision(
    *,
    user_message: str,
    conversation_history: Any,
    model: str,
    platform: str,
) -> _RouteDecision | None:
    max_chars = _env_int("JEV_FASTLANE_STATE_MAX_CHARS", 10000, minimum=500, maximum=30000)
    message = _redact_text(user_message.strip())[:max_chars]
    state = {
        "user_message": message,
        "recent_context": _recent_context(conversation_history, user_message),
        "surface": platform or "unknown",
        "active_model": model or "unknown",
    }
    body = _call_jev(state=state, questions=_route_questions(), cacheable=True)
    if body is None:
        return None
    answers = body.get("answers")
    if not isinstance(answers, dict):
        return None
    intent, intent_conf = _choice(answers, "intent")
    response_length, _ = _choice(answers, "response_length", "normal")
    return _RouteDecision(
        intent=intent,
        intent_confidence=intent_conf,
        requires_tools=_noul(answers, "requires_tools"),
        requires_current_data=_noul(answers, "requires_current_data"),
        mutation_intent=_noul(answers, "mutation_intent"),
        needs_deep_reasoning=_noul(answers, "needs_deep_reasoning"),
        needs_post_action_verification=_noul(answers, "needs_post_action_verification"),
        risk_score=_score(answers, "risk"),
        response_length=response_length,
        resolved_model=str(body.get("model") or ""),
        latency_ms=int(body.get("_fastlane_latency_ms") or 0),
        input_tokens=int(body.get("_fastlane_input_tokens") or 0),
    )


def _is_confident_toolless(route: _RouteDecision) -> bool:
    return (
        route.intent == "direct_answer"
        and route.intent_confidence >= _env_float("JEV_FASTLANE_DIRECT_CONFIDENCE", 0.97, minimum=0.5, maximum=1.0)
        and route.requires_tools <= 0.03
        and route.requires_current_data <= 0.03
        and route.mutation_intent <= 0.02
    )


def _route_context(route: _RouteDecision) -> str:
    directives: list[str] = []
    if _is_confident_toolless(route):
        directives.append("answer directly; no tools or browsing")
    elif route.requires_tools >= 0.65 or route.requires_current_data >= 0.65:
        directives.append("use only the minimum necessary tools; batch independent reads; stop when evidence is sufficient")
    else:
        directives.append("avoid tools unless they materially improve correctness")

    if route.requires_current_data >= 0.65:
        directives.append("verify current facts externally")
    if route.mutation_intent >= 0.65:
        directives.append("before persistent/external writes verify exact target and rollback path; after action verify resulting state")
    if route.needs_post_action_verification >= 0.70:
        directives.append("never claim an action succeeded without post-action evidence")
    if route.risk_score >= 2.0:
        directives.append("fail closed on ambiguous or irreversible targets")
    if route.needs_deep_reasoning < 0.25:
        directives.append("keep reasoning bounded")

    length = route.response_length if route.response_length in {"brief", "normal", "detailed"} else "normal"
    directive_text = "; ".join(directives)
    return (
        "[JEV_FASTLANE] "
        f"intent={route.intent}; response={length}; risk={route.risk_score:.2f}/3; "
        f"policy={directive_text}."
    )


def _clear_tool_whitelist() -> None:
    try:
        from hermes_cli.plugins import clear_thread_tool_whitelist

        clear_thread_tool_whitelist()
    except Exception:
        pass


def _set_no_tools_whitelist() -> None:
    try:
        from hermes_cli.plugins import set_thread_tool_whitelist

        set_thread_tool_whitelist(
            set(),
            "Tool '{tool_name}' denied by Jev Fastlane: this turn was classified with very high confidence as a direct, stable, tool-free answer.",
        )
    except Exception:
        pass


def _pre_llm_call(
    session_id: str = "",
    user_message: Any = "",
    conversation_history: Any = None,
    model: str = "",
    platform: str = "",
    **_: Any,
) -> dict[str, str] | None:
    _clear_tool_whitelist()
    if not _enabled() or not isinstance(user_message, str) or not user_message.strip():
        return None

    route = _route_decision(
        user_message=user_message,
        conversation_history=conversation_history,
        model=model,
        platform=platform,
    )
    if route is None:
        return None

    if session_id:
        with _runtime.lock:
            _runtime.routes_by_session[session_id] = (route, _redact_text(user_message)[:12000])

    if _is_confident_toolless(route):
        _set_no_tools_whitelist()

    return {"context": _route_context(route)}


def _terminal_command(args: Any) -> str:
    if not isinstance(args, dict):
        return ""
    for key in ("command", "cmd", "shell", "script"):
        value = args.get(key)
        if isinstance(value, str):
            return value
    return ""


def _is_high_risk_mutation(tool_name: str, args: Any) -> bool:
    name = tool_name or ""
    if name == "terminal":
        return bool(_MUTATING_TERMINAL_RE.search(_terminal_command(args)))
    return bool(_EXTERNAL_MUTATION_TOOL_RE.search(name))


def _catastrophic_block(tool_name: str, args: Any) -> str | None:
    if tool_name != "terminal":
        return None
    command = _terminal_command(args)
    if _CATASTROPHIC_TERMINAL_RE.search(command):
        return "Jev Fastlane blocked a catastrophic shell pattern. Use a scoped, reversible command with an explicit target instead."
    return None


def _mutation_questions() -> dict[str, Any]:
    return {
        "matches_user_intent": {
            "type": "noul",
            "instructions": "Does this exact proposed tool call directly implement the user's latest explicit request rather than going beyond it?",
        },
        "target_is_unambiguous": {
            "type": "noul",
            "instructions": "Is the action target clearly identified and consistent with what the user asked to change?",
        },
        "needs_confirmation": {
            "type": "noul",
            "instructions": "Should execution pause for explicit human confirmation now? Treat a clear latest user instruction to perform this exact kind of action on this target as confirmation already given.",
        },
        "destructive_or_external_write": {
            "type": "noul",
            "instructions": "Will this call delete, publish, deploy, send, overwrite, mutate production/external state, or otherwise create a meaningful side effect?",
        },
        "readily_reversible": {
            "type": "noul",
            "instructions": "Can this action be reversed reliably with low risk using an existing backup, version history, rollback, or inverse operation?",
        },
    }


def _mutation_gate(
    *,
    route: _RouteDecision | None,
    user_message: str,
    tool_name: str,
    args: Any,
) -> str | None:
    if not _enabled():
        return None
    safe_args = _sanitize_value(args)
    state = {
        "latest_user_request": _redact_text(user_message)[:10000],
        "route": {
            "intent": route.intent if route else "unknown",
            "mutation_intent_probability": route.mutation_intent if route else None,
            "risk_score_0_to_3": route.risk_score if route else None,
        },
        "proposed_tool": tool_name,
        "proposed_arguments": safe_args,
    }
    body = _call_jev(state=state, questions=_mutation_questions(), cacheable=False)
    if body is None:
        return None
    answers = body.get("answers")
    if not isinstance(answers, dict):
        return None

    matches = _noul(answers, "matches_user_intent")
    target = _noul(answers, "target_is_unambiguous")
    confirm = _noul(answers, "needs_confirmation")
    destructive = _noul(answers, "destructive_or_external_write")
    reversible = _noul(answers, "readily_reversible")
    mutation_intent = route.mutation_intent if route else 0.5

    min_match = _env_float("JEV_FASTLANE_MUTATION_MATCH_MIN", 0.78, minimum=0.5, maximum=0.99)
    if matches < min_match:
        return f"Jev Fastlane blocked '{tool_name}': proposed action does not confidently match the latest user request ({matches:.2f}). Re-check the requested action and target."
    if target < min_match:
        return f"Jev Fastlane blocked '{tool_name}': target is ambiguous ({target:.2f}). Resolve the exact target before mutating state."
    if confirm >= 0.78:
        return f"Jev Fastlane blocked '{tool_name}': this side effect needs explicit confirmation before execution ({confirm:.2f})."
    if destructive >= 0.82 and reversible <= 0.30 and mutation_intent < 0.85:
        return (
            f"Jev Fastlane blocked '{tool_name}': high-impact/irreversible mutation was not clearly requested "
            f"(destructive={destructive:.2f}, reversible={reversible:.2f}, mutation_intent={mutation_intent:.2f})."
        )
    return None


def _pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    session_id: str = "",
    **_: Any,
) -> dict[str, str] | None:
    catastrophic = _catastrophic_block(tool_name, args)
    if catastrophic:
        return {"action": "block", "message": catastrophic}
    if not _is_high_risk_mutation(tool_name, args):
        return None

    route: _RouteDecision | None = None
    user_message = ""
    if session_id:
        with _runtime.lock:
            stored = _runtime.routes_by_session.get(session_id)
        if stored is not None:
            route, user_message = stored
    if not user_message:
        return None

    message = _mutation_gate(
        route=route,
        user_message=user_message,
        tool_name=tool_name,
        args=args,
    )
    if message:
        return {"action": "block", "message": message}
    return None


def _cleanup_session(session_id: str = "", **_: Any) -> None:
    _clear_tool_whitelist()
    if session_id:
        with _runtime.lock:
            _runtime.routes_by_session.pop(session_id, None)


def _status_text() -> str:
    now = time.monotonic()
    with _runtime.lock:
        calls = _runtime.calls
        avg_ms = round(_runtime.total_latency_ms / calls) if calls else 0
        hit_total = calls + _runtime.cache_hits
        hit_rate = (_runtime.cache_hits / hit_total * 100.0) if hit_total else 0.0
        circuit_left = max(0, int(round(_runtime.circuit_open_until - now)))
        return (
            "Jev Fastlane\n"
            f"enabled: {_runtime.runtime_enabled and _env_bool('JEV_FASTLANE_ENABLED', True)}\n"
            f"api_key: {'configured' if _configured() else 'missing'}\n"
            f"model: {os.getenv('JEV_FASTLANE_MODEL', os.getenv('TYPESAFE_DEFAULT_MODEL', _DEFAULT_MODEL))}\n"
            f"timeout_ms: {_env_int('JEV_FASTLANE_TIMEOUT_MS', 450, minimum=100, maximum=5000)}\n"
            f"calls: {calls} | cache_hits: {_runtime.cache_hits} ({hit_rate:.1f}%) | failures: {_runtime.failures}\n"
            f"avg_latency_ms: {avg_ms} | input_tokens: {_runtime.total_input_tokens}\n"
            f"resolved_model: {_runtime.last_model or '-'}\n"
            f"circuit: {'OPEN ' + str(circuit_left) + 's' if circuit_left else 'closed'}\n"
            f"last_error: {_runtime.last_error or '-'}"
        )


def _command(raw_args: str) -> str:
    sub = (raw_args or "status").strip().lower()
    if sub in {"", "status"}:
        return _status_text()
    if sub == "on":
        _runtime.runtime_enabled = True
        return "Jev Fastlane enabled for this Hermes process."
    if sub == "off":
        _runtime.runtime_enabled = False
        _clear_tool_whitelist()
        return "Jev Fastlane disabled for this Hermes process."
    if sub == "reset":
        with _runtime.lock:
            _runtime.cache.clear()
            _runtime.routes_by_session.clear()
            _runtime.failures_in_row = 0
            _runtime.circuit_open_until = 0.0
            _runtime.calls = 0
            _runtime.cache_hits = 0
            _runtime.failures = 0
            _runtime.total_latency_ms = 0
            _runtime.total_input_tokens = 0
            _runtime.last_error = ""
            _runtime.last_model = ""
        _clear_tool_whitelist()
        return "Jev Fastlane cache, circuit breaker, and telemetry reset."
    return "Usage: /jev-fastlane [status|on|off|reset]"


def register(ctx: Any) -> None:
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_hook("pre_tool_call", _pre_tool_call)
    ctx.register_hook("post_llm_call", _cleanup_session)
    ctx.register_hook("on_session_end", _cleanup_session)
    ctx.register_hook("on_session_reset", _cleanup_session)
    ctx.register_hook("on_session_finalize", _cleanup_session)
    ctx.register_command(
        "jev-fastlane",
        _command,
        description="Jev routing/guardrail status and runtime toggle",
        args_hint="[status|on|off|reset]",
    )
