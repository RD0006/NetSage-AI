def check_interfaces(command_outputs):
    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show ip interface brief" not in command:
            continue

        for line in output.splitlines():

            parts = line.split()

            if len(parts) < 6:
                continue

            interface = parts[0]
            status = parts[-2]
            protocol = parts[-1]

            # Check administrative shutdown FIRST
            if "administratively" in line and status == "down":
                issues.append({
                    "type": "interface_shutdown",
                    "interface": interface,
                    "message": f"{interface} is administratively down."
                })

            # Then check normal interface/protocol down
            elif status == "down" or protocol == "down":
                issues.append({
                    "type": "interface_down",
                    "interface": interface,
                    "message": f"{interface} is down."
                })

    return issues