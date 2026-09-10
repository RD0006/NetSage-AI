def check_nat(command_outputs):
    issues = []

    for item in command_outputs:
        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show ip nat translations" not in command:
            continue

        lines = [
            line.strip()
            for line in output.splitlines()
            if line.strip()
        ]

        # No output at all
        if not lines:
            issues.append({
                "type": "nat_translation_missing",
                "message": "No active NAT translations were detected."
            })
            continue

        # Find actual translation entries.
        # The first line is normally the table header beginning with "Pro".
        translation_entries = [
            line for line in lines[1:]
            if line and not line.startswith("-")
        ]

        if not translation_entries:
            issues.append({
                "type": "nat_translation_missing",
                "message": "No active NAT translations were detected."
            })

    return issues
