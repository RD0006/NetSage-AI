def check_dns(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show running-config" not in command:
            continue

        if "ip name-server" not in output:
            issues.append({
                "type": "dns_missing",
                "message": "No DNS name-server configuration detected."
            })

    return issues