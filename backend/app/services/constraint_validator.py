def validate_transform(*, snapshot, target, operation, params, constraints):
    violations = []

    for constraint in constraints:
        if constraint.startswith("locked_axis"):
            axis = constraint.split(":")[1]
            if axis in params and params.get(axis, 0) != 0:
                violations.append({
                    "constraint": "locked_axis",
                    "message": f"Axis {axis} is locked",
                })

        if constraint.startswith("symmetry"):
            plane = constraint.split(":")[1]
            if not snapshot.is_symmetric(target, plane, params):
                violations.append({
                    "constraint": "symmetry",
                    "message": f"Target must remain symmetric across {plane}",
                })

    return violations

