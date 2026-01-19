ALLOWED_LEVEL2_PARAMS = {
    "length",
    "height",
    "width",
    "rake",
    "roof_arc",
}

def normalize_params(params):
    return {
        k: v
        for k, v in (params or {}).items()
        if k in ALLOWED_LEVEL2_PARAMS
    }

