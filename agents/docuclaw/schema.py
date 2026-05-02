"""DocuClaw Schema - Constitutional contract for document operations."""
def validate(payload: dict) -> dict:
    if not isinstance(payload, dict): return {"valid": False, "error": "Payload must be a dict"}
    if payload.get("type") == "delegate":
        if "target_agent" not in payload: return {"valid": False, "error": "Delegate requires target_agent"}
        return {"valid": True, "payload": payload}
    payload.setdefault("type", "document"); payload.setdefault("intent", "create_document")
    payload.setdefault("confidence", 1.0); payload.setdefault("source", "user"); payload.setdefault("query", "")
    return {"valid": True, "payload": payload}
