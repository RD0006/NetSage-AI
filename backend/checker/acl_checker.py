def check_acls(command_outputs):
    issues = []

    for item in command_outputs:
        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show access-lists" not in command:
            continue

        # Detect both:
        # "access-list 10"
        # "access list 10"
        if not output.strip() or (
            "access-list" not in output
            and "access list" not in output
        ):
            issues.append({
                "type": "acl_missing",
                "message": "No access-control lists were detected."
            })

    return issues
