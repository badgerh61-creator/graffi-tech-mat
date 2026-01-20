def emit_event(event_type, payload, trace_id=None):
    # Stub: forward to log sink
    return {
        "event_type": event_type,
        "payload": payload,
        "trace_id": trace_id,
    }

