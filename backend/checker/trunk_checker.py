def check_trunks(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show interfaces trunk" not in command:
            continue

        if not output.strip():
            issues.append({
                "type": "trunk_missing",
                "message": "No trunk interfaces were detected."
            })

    return issues