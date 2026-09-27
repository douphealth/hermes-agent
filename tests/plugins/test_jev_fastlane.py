import importlib.util
import sys
from pathlib import Path


def load_plugin():
    path = Path(__file__).resolve().parents[2] / "plugins" / "jev-fastlane" / "__init__.py"
    spec = importlib.util.spec_from_file_location("jev_fastlane_test", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_redacts_credentials():
    mod = load_plugin()
    text = "Authorization: Bearer abcdefghijklmnop password=hunter2 token=supersecretvalue 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabc"
    out = mod._redact_text(text)
    assert "abcdefghijklmnop" not in out
    assert "hunter2" not in out
    assert "supersecretvalue" not in out
    assert "ABCDEFGHIJKLMNOPQRSTUVWXYZabc" not in out


def test_sanitize_secret_keys():
    mod = load_plugin()
    out = mod._sanitize_value({"username": "admin", "api_key": "sekret", "nested": {"application_password": "x"}})
    assert out["username"] == "admin"
    assert out["api_key"] == "[REDACTED]"
    assert out["nested"]["application_password"] == "[REDACTED]"


def test_route_decision_single_batched_call(monkeypatch):
    mod = load_plugin()
    body = {
        "model": "jev-1.13.0",
        "answers": {
            "intent": {"type": "choice", "choice": "direct_answer", "confidence": 0.99},
            "requires_tools": {"type": "noul", "noul": 0.01},
            "requires_current_data": {"type": "noul", "noul": 0.01},
            "mutation_intent": {"type": "noul", "noul": 0.0},
            "needs_deep_reasoning": {"type": "noul", "noul": 0.05},
            "needs_post_action_verification": {"type": "noul", "noul": 0.05},
            "risk": {"type": "score", "score": 0.1},
            "response_length": {"type": "choice", "choice": "brief", "confidence": 0.95},
        },
        "_fastlane_latency_ms": 101,
        "_fastlane_input_tokens": 155,
    }
    calls = []

    def fake_call(**kwargs):
        calls.append(kwargs)
        return body

    monkeypatch.setattr(mod, "_call_jev", fake_call)
    route = mod._route_decision(user_message="What is a canonical URL?", conversation_history=[], model="gpt-x", platform="telegram")
    assert len(calls) == 1
    assert len(calls[0]["questions"]) == 8
    assert route.intent == "direct_answer"
    assert mod._is_confident_toolless(route) is True
    assert "no tools or browsing" in mod._route_context(route)


def test_high_risk_detection_is_selective():
    mod = load_plugin()
    assert mod._is_high_risk_mutation("terminal", {"command": "git status"}) is False
    assert mod._is_high_risk_mutation("terminal", {"command": "git push origin main"}) is True
    assert mod._is_high_risk_mutation("write_file", {"path": "a.py"}) is False
    assert mod._is_high_risk_mutation("wordpress_update_post", {"id": 4}) is True


def test_catastrophic_terminal_fails_closed():
    mod = load_plugin()
    message = mod._catastrophic_block("terminal", {"command": "sudo rm -rf /"})
    assert message is not None


def test_mutation_gate_blocks_ambiguous_target(monkeypatch):
    mod = load_plugin()
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    body = {
        "answers": {
            "matches_user_intent": {"type": "noul", "noul": 0.96},
            "target_is_unambiguous": {"type": "noul", "noul": 0.41},
            "needs_confirmation": {"type": "noul", "noul": 0.2},
            "destructive_or_external_write": {"type": "noul", "noul": 0.9},
            "readily_reversible": {"type": "noul", "noul": 0.8},
        }
    }
    monkeypatch.setattr(mod, "_call_jev", lambda **_: body)
    msg = mod._mutation_gate(route=None, user_message="Update my site", tool_name="wordpress_update_post", args={"id": 7})
    assert "target is ambiguous" in msg


def test_mutation_gate_allows_explicit_reversible_action(monkeypatch):
    mod = load_plugin()
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-key")
    body = {
        "answers": {
            "matches_user_intent": {"type": "noul", "noul": 0.98},
            "target_is_unambiguous": {"type": "noul", "noul": 0.99},
            "needs_confirmation": {"type": "noul", "noul": 0.1},
            "destructive_or_external_write": {"type": "noul", "noul": 0.8},
            "readily_reversible": {"type": "noul", "noul": 0.95},
        }
    }
    monkeypatch.setattr(mod, "_call_jev", lambda **_: body)
    route = mod._RouteDecision("wordpress_write", 0.99, 0.99, 0.4, 0.99, 0.5, 0.99, 2.0, "normal", "jev", 80, 100)
    msg = mod._mutation_gate(route=route, user_message="Update post 7 now", tool_name="wordpress_update_post", args={"id": 7})
    assert msg is None
