import re


def check_routes(command_outputs):
    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "")

        if "show ip route" not in command:
            continue

        # Detect explicit statements indicating a missing route
        for line in output.splitlines():

            line_lower = line.lower()

            if "not present in the routing table" in line_lower:
                match = re.search(
                    r"(\d+\.\d+\.\d+\.\d+/\d+)",
                    line
                )

                if match:
                    network = match.group(1)

                    issues.append({
                        "type": "missing_route",
                        "network": network,
                        "message": (
                            f"Route to {network} is missing "
                            "from the routing table."
                        )
                    })

    return issues