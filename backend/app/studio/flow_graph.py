FLOW_GRAPH = {
    "start": {"transform"},
    "transform": {"transform", "constraint", "validate"},
    "constraint": {"transform", "validate"},
    "validate": {"finalize"},
    "finalize": set(),
}

