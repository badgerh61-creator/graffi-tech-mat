def test_trace_id_propagation(
    trace_context,
):
    with trace_context.start_span("geometry.regeneration") as span:
        assert span.trace_id is not None

