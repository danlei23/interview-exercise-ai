import json

ALLOWED_ACTIONS = {
    "no_action", "request_more_info", "escalate_to_billing", "escalate_to_abuse_team"
}

def coerce_json(s: str) -> dict:
    s = s.strip()
    # Remove the ```json ... ``` wrappers
    if s.startswith("```") and s.endswith("```"):
        s = s.strip("`\n ")
        if s.startswith("json"):
            s = s[4:].strip()
    i, j = s.find("{"), s.rfind("}")
    if i >= 0 and j > i:
        s = s[i:j+1]
    return json.loads(s)

def ensure_mcp(payload: dict) -> dict:
    # Whitelist of allowed 'action_required' values
    if payload.get("action_required") not in ALLOWED_ACTIONS:
        payload["action_required"] = "request_more_info"
    payload.setdefault("references", [])
    payload.setdefault("answer", "")
    return payload
