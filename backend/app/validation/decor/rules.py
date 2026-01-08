def validate_uv_transform(uv: dict):
    x = uv.get("x")
    y = uv.get("y")
    scale = uv.get("scale")
    rotation = uv.get("rotation")

    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        return False, "UV x/y must be between 0.0 and 1.0"

    if not (0.0 < scale <= 2.0):
        return False, "UV scale must be between 0.0 and 2.0"

    if not (-180 <= rotation <= 180):
        return False, "UV rotation must be between -180 and 180"

    return True, None


def validate_material(material: dict):
    color = material.get("color")
    finish = material.get("finish")

    if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
        return False, "Material color must be valid hex (#RRGGBB)"

    if finish not in {"matte", "gloss", "metallic"}:
        return False, "Invalid material finish"

    return True, None

