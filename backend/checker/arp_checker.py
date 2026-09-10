def check_arp(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show ip arp" not in command:
            continue

        if not output.strip():
            issues.append({
                "type": "arp_missing",
                "message": "ARP table is empty."
            })

    return issues