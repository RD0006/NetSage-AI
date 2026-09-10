def check_dhcp(command_outputs):
    issues = []

    for item in command_outputs:
        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show ip dhcp pool" not in command:
            continue

        # A real DHCP pool should have a pool declaration,
        # not merely the word "pool" in an error message.
        if "pool " not in output or "no dhcp pool" in output:
            issues.append({
                "type": "dhcp_pool_missing",
                "message": "No DHCP pool configuration detected."
            })
            continue

        if "network" not in output:
            issues.append({
                "type": "dhcp_network_missing",
                "message": "DHCP pool does not contain a network configuration."
            })

    return issues
