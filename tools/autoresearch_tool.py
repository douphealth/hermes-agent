#!/usr/bin/env python3
"""Autoresearch tool: autonomous experiment-loop primitives for agents.

This is a small, dependency-free implementation of the core pattern from
karpathy/autoresearch generalized for Hermes:

1. isolate a run on a branch;
2. let the agent edit a constrained target surface;
3. run a bounded experiment with logs captured off-context;
4. parse a scalar metric;
5. keep the commit only when it improves the best known result, otherwise
   reset back to the previous commit;
6. append a TSV ledger for durable, cheap progress tracking.

The tool deliberately does not edit code itself. Hermes already has file/patch
and coding-agent tools for that. This tool makes the scientific loop reliable,
cheap, and repeatable.
"""

from __future__ import annotations

import csv
import json
import os
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from tools.registry import registry, tool_error, tool_result


DEFAULT_RESULTS_HEADER = ["commit", "metric", "memory_gb", "status", "description"]
DEFAULT_METRIC_REGEX = r"^val_bpb:\s*([0-9]+(?:\.[0-9]+)?)"
DEFAULT_MEMORY_REGEX = r"^peak_vram_mb:\s*([0-9]+(?:\.[0-9]+)?)"


@dataclass(frozen=True)
class ExperimentResult:
    status: str
    metric: float
    memory_gb: float
    commit: str
    improved: bool
    returncode: int | None
    timeout: bool
    log_file: str
    decision: str


def _jsonable_error(message: str, **extra: Any) -> str:
    return tool_error(message, success=False, **extra)


def _repo(repo_path: str) -> Path:
    if not repo_path:
        raise ValueError("repo_path is required")
    path = Path(repo_path).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"repo_path is not a directory: {path}")
    git = path / ".git"
    if not git.exists():
        raise ValueError(f"repo_path is not a git repository: {path}")
    return path


def _run_git(repo: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            "git " + " ".join(args) + " failed: " + (proc.stderr.strip() or proc.stdout.strip())
        )
    return proc


def _short_head(repo: Path) -> str:
    return _run_git(repo, ["rev-parse", "--short=7", "HEAD"]).stdout.strip()


def _head(repo: Path) -> str:
    return _run_git(repo, ["rev-parse", "HEAD"]).stdout.strip()


def _current_branch(repo: Path) -> str:
    return _run_git(repo, ["branch", "--show-current"]).stdout.strip()


def _rel(repo: Path, value: str) -> str:
    p = Path(value)
    if p.is_absolute():
        try:
            return str(p.resolve().relative_to(repo))
        except ValueError as exc:
            raise ValueError(f"path must be inside repo: {value}") from exc
    return str(p)


def _status_entries(repo: Path) -> list[tuple[str, str]]:
    out = _run_git(repo, ["status", "--porcelain=v1"], check=True).stdout
    entries: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line:
            continue
        status = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append((status, path))
    return entries


def _dirty_allowed(repo: Path, editable_files: Iterable[str], ignored_files: Iterable[str]) -> tuple[bool, list[str]]:
    editable = {_rel(repo, p) for p in editable_files if p}
    ignored = {_rel(repo, p) for p in ignored_files if p}
    offenders = []
    for status, path in _status_entries(repo):
        if path in editable or path in ignored:
            continue
        offenders.append(f"{status} {path}")
    return not offenders, offenders


def _ensure_results(path: Path) -> None:
    if not path.exists() or not path.read_text(encoding="utf-8", errors="replace").strip():
        path.write_text("\t".join(DEFAULT_RESULTS_HEADER) + "\n", encoding="utf-8")


def _read_best(results_path: Path, goal: str) -> float | None:
    if not results_path.exists():
        return None
    best: float | None = None
    with results_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not reader.fieldnames:
            return None
        metric_field = "metric" if "metric" in reader.fieldnames else "val_bpb"
        for row in reader:
            if row.get("status") != "keep":
                continue
            try:
                value = float(row.get(metric_field) or 0)
            except ValueError:
                continue
            if value <= 0:
                continue
            if best is None:
                best = value
            elif goal == "min" and value < best:
                best = value
            elif goal == "max" and value > best:
                best = value
    return best


def _is_improved(metric: float, best_before: float | None, goal: str, min_delta: float) -> bool:
    if metric <= 0:
        return False
    if best_before is None:
        return True
    if goal == "min":
        return metric < (best_before - min_delta)
    return metric > (best_before + min_delta)


def _parse_first_float(pattern: str, text: str) -> float | None:
    flags = re.MULTILINE
    match = re.search(pattern, text, flags)
    if not match:
        return None
    try:
        return float(match.group(1))
    except (IndexError, ValueError):
        return None


def _append_result(results_path: Path, result: ExperimentResult, description: str) -> None:
    _ensure_results(results_path)
    safe_description = " ".join(str(description or "experiment").split())
    with results_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow([
            result.commit,
            f"{result.metric:.6f}",
            f"{result.memory_gb:.1f}",
            result.status,
            safe_description,
        ])


def _setup(args: dict[str, Any]) -> str:
    repo = _repo(str(args.get("repo_path") or ""))
    run_tag = str(args.get("run_tag") or "").strip()
    branch = str(args.get("branch") or "").strip()
    if not branch:
        if not run_tag:
            raise ValueError("Provide branch or run_tag")
        branch = f"autoresearch/{run_tag}"
    if not re.match(r"^[A-Za-z0-9._/-]+$", branch):
        raise ValueError("branch contains unsupported characters")

    results_file = _rel(repo, str(args.get("results_file") or "results.tsv"))
    results_path = repo / results_file

    exists = _run_git(repo, ["rev-parse", "--verify", branch], check=False).returncode == 0
    if exists and not bool(args.get("reuse_existing", False)):
        return _jsonable_error("branch already exists", branch=branch)
    if exists:
        _run_git(repo, ["checkout", branch])
    else:
        _run_git(repo, ["checkout", "-b", branch])
    _ensure_results(results_path)

    return tool_result(
        success=True,
        action="setup",
        repo_path=str(repo),
        branch=_current_branch(repo),
        head=_short_head(repo),
        results_file=results_file,
        message="Autoresearch branch and TSV ledger are ready.",
    )


def _commit_editable_changes(repo: Path, editable_files: list[str], description: str) -> tuple[bool, str, str]:
    before = _head(repo)
    # Stage only the declared experiment surface.
    paths_to_add = [p for p in editable_files if (repo / p).exists()]
    if paths_to_add:
        _run_git(repo, ["add", "--", *paths_to_add])
    diff_cached = _run_git(repo, ["diff", "--cached", "--quiet"], check=False)
    if diff_cached.returncode == 0:
        return False, before, _short_head(repo)
    msg = "autoresearch: " + (" ".join(str(description or "experiment").split())[:180] or "experiment")
    _run_git(repo, ["commit", "-m", msg])
    return True, before, _short_head(repo)


def _run_once(args: dict[str, Any]) -> str:
    repo = _repo(str(args.get("repo_path") or ""))
    command = str(args.get("run_command") or "").strip()
    if not command:
        raise ValueError("run_command is required")

    description = str(args.get("description") or "experiment")
    target_file = str(args.get("target_file") or "train.py")
    extra_files = args.get("editable_files") or []
    if isinstance(extra_files, str):
        extra_files = [extra_files]
    editable_files = []
    for p in [target_file, *list(extra_files)]:
        rel = _rel(repo, str(p))
        if rel not in editable_files:
            editable_files.append(rel)

    results_file = _rel(repo, str(args.get("results_file") or "results.tsv"))
    log_file = _rel(repo, str(args.get("log_file") or "run.log"))
    results_path = repo / results_file
    log_path = repo / log_file
    metric_regex = str(args.get("metric_regex") or DEFAULT_METRIC_REGEX)
    memory_regex = str(args.get("memory_regex") or DEFAULT_MEMORY_REGEX)
    goal = str(args.get("goal") or "min").lower()
    if goal not in {"min", "max"}:
        raise ValueError("goal must be 'min' or 'max'")
    min_delta = float(args.get("min_delta") or 0.0)
    timeout_seconds = int(args.get("timeout_seconds") or 600)
    if timeout_seconds < 1 or timeout_seconds > 86400:
        raise ValueError("timeout_seconds must be between 1 and 86400")

    ok, offenders = _dirty_allowed(repo, editable_files, ignored_files=[results_file, log_file])
    if not ok:
        return _jsonable_error(
            "Working tree has dirty files outside the declared editable surface; refusing to risk data loss.",
            offenders=offenders,
            editable_files=editable_files,
        )

    _ensure_results(results_path)
    best_before = _read_best(results_path, goal)
    created_commit, start_commit, experiment_commit = _commit_editable_changes(repo, editable_files, description)

    timeout = False
    returncode: int | None
    combined = ""
    try:
        proc = subprocess.run(
            command,
            cwd=str(repo),
            shell=True,
            executable="/bin/bash",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
        )
        returncode = proc.returncode
        combined = proc.stdout or ""
    except subprocess.TimeoutExpired as exc:
        timeout = True
        returncode = None
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        combined = out + f"\n[TIMEOUT after {timeout_seconds}s]\n"

    log_path.write_text(combined, encoding="utf-8", errors="replace")
    metric = _parse_first_float(metric_regex, combined)
    memory_mb = _parse_first_float(memory_regex, combined)
    memory_gb = (memory_mb or 0.0) / 1024.0

    crashed = timeout or returncode not in (0, None) or metric is None
    metric_value = float(metric or 0.0)
    improved = (not crashed) and _is_improved(metric_value, best_before, goal, min_delta)

    if crashed:
        status = "crash"
        decision = "discarded crash/timeout/no metric"
    elif improved:
        status = "keep"
        decision = "kept improvement"
    else:
        status = "discard"
        decision = "discarded non-improvement"

    result = ExperimentResult(
        status=status,
        metric=metric_value,
        memory_gb=memory_gb,
        commit=experiment_commit,
        improved=improved,
        returncode=returncode,
        timeout=timeout,
        log_file=log_file,
        decision=decision,
    )
    _append_result(results_path, result, description)

    reset_performed = False
    if created_commit and status != "keep":
        _run_git(repo, ["reset", "--hard", start_commit])
        reset_performed = True

    return tool_result(
        success=True,
        action="run_once",
        repo_path=str(repo),
        branch=_current_branch(repo),
        start_commit=start_commit[:7],
        experiment_commit=experiment_commit,
        current_head=_short_head(repo),
        created_commit=created_commit,
        status=status,
        improved=improved,
        best_before=best_before,
        metric=metric_value,
        metric_goal=goal,
        memory_gb=round(memory_gb, 3),
        returncode=returncode,
        timeout=timeout,
        reset_performed=reset_performed,
        results_file=results_file,
        log_file=log_file,
        command=command,
        command_preview=shlex.join(["bash", "-lc", command])[:500],
        decision=decision,
    )


def autoresearch(args: dict[str, Any], **_: Any) -> str:
    """Dispatch the autoresearch tool."""
    action = str(args.get("action") or "run_once").strip().lower()
    try:
        if action == "setup":
            return _setup(args)
        if action == "run_once":
            return _run_once(args)
        return _jsonable_error("Unknown action", action=action, valid_actions=["setup", "run_once"])
    except Exception as exc:
        return _jsonable_error(str(exc), action=action)


AUTORESEARCH_SCHEMA = {
    "name": "autoresearch",
    "description": (
        "Run an autonomous research/experiment loop step inspired by karpathy/autoresearch. "
        "Use after editing a target file: it commits only the declared experiment surface, runs a "
        "bounded command with output captured to a log file, parses a scalar metric, appends a TSV "
        "ledger, keeps improvements, and git-resets failed or worse commits. This is for efficient "
        "SOTA agent self-improvement/benchmark/search loops, not for arbitrary shell work."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["setup", "run_once"], "default": "run_once"},
            "repo_path": {"type": "string", "description": "Path to a git repository."},
            "run_tag": {"type": "string", "description": "Setup only: creates branch autoresearch/<run_tag>."},
            "branch": {"type": "string", "description": "Setup only: explicit branch name to create/checkout."},
            "reuse_existing": {"type": "boolean", "default": False},
            "target_file": {"type": "string", "default": "train.py", "description": "Primary editable experiment file."},
            "editable_files": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Additional files the tool may stage/commit/reset for this experiment.",
            },
            "run_command": {"type": "string", "description": "Bounded experiment command, e.g. 'uv run train.py'."},
            "metric_regex": {
                "type": "string",
                "default": DEFAULT_METRIC_REGEX,
                "description": "Regex with capture group 1 as the scalar metric.",
            },
            "memory_regex": {
                "type": "string",
                "default": DEFAULT_MEMORY_REGEX,
                "description": "Optional regex with capture group 1 as peak memory in MB.",
            },
            "goal": {"type": "string", "enum": ["min", "max"], "default": "min"},
            "min_delta": {"type": "number", "default": 0.0},
            "timeout_seconds": {"type": "integer", "default": 600},
            "results_file": {"type": "string", "default": "results.tsv"},
            "log_file": {"type": "string", "default": "run.log"},
            "description": {"type": "string", "description": "Short TSV/commit description of the experiment."},
        },
        "required": ["repo_path"],
    },
}


registry.register(
    name="autoresearch",
    toolset="autoresearch",
    schema=AUTORESEARCH_SCHEMA,
    handler=autoresearch,
    description=AUTORESEARCH_SCHEMA["description"],
    emoji="🧪",
    max_result_size_chars=8000,
)
