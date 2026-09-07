def check_routes(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show ip route" not in command:
            continue

        if "gateway of last resort is not set" in output:

            issues.append({
                "type": "missing_default_route",
                "message": "Default route/gateway is not configured."
            })

    return issues