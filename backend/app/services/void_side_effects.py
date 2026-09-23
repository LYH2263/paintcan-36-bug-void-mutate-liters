"""Side effects applied when a run is voided."""
import json


def blank_liters_result(result):
    out = dict(result or {})
    for key in ("liters", "total_liters", "wall_liters", "ceiling_liters"):
        if key in out:
            out[key] = 0.0
    out["void_cleared"] = True
    return out


def zero_result_json(raw):
    try:
        data = json.loads(raw) if isinstance(raw, str) else dict(raw or {})
    except (TypeError, ValueError, json.JSONDecodeError):
        data = {}
    return json.dumps(blank_liters_result(data), ensure_ascii=False)


def apply_live_clear(conn, run_id, get_fn, estimate_fn=None):
    row = get_fn(conn, run_id)
    if not row:
        return None
    return blank_liters_result(json.loads(row["result_json"]) if isinstance(row.get("result_json"), str) else row.get("result_json"))
