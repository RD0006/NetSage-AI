def check_connectivity(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if not command.startswith("ping"):
            continue

        if "success rate is 0 percent" in output:
            issues.append({
                "type": "connectivity_failure",
                "message": "Ping failed completely."
            })

        elif "unreachable" in output:
            issues.append({
                "type": "host_unreachable",
                "message": "Destination host is unreachable."
            })

    return issues