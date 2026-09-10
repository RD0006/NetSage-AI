def check_interfaces(command_outputs):
    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "")

        if "show ip interface brief" not in command:
            continue

        for line in output.splitlines():

            parts = line.split()

            if len(parts) < 6:
                continue

            interface = parts[0]
            ip_address = parts[1]
            status = parts[-2].lower()
            protocol = parts[-1].lower()

            # Ignore interfaces that are not configured
            if ip_address.lower() == "unassigned":
                continue

            # Check administratively down
            if "administratively" in line.lower() and status == "down":
                issues.append({
                    "type": "interface_shutdown",
                    "interface": interface,
                    "message": f"{interface} is administratively down."
                })

            # Check normal interface/protocol down
            elif status == "down" or protocol == "down":
                issues.append({
                    "type": "interface_down",
                    "interface": interface,
                    "message": f"{interface} is down."
                })

    return issues