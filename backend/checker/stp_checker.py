def check_stp(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show spanning-tree" not in command:
            continue

        # Check for STP root bridge information
        if "root" not in output:
            issues.append({
                "type": "stp_root_missing",
                "message": "No STP root bridge information detected."
            })

        # Cisco commonly uses "BLK" for blocking state
        if "blocking" in output or " blk" in output:
            issues.append({
                "type": "stp_blocking",
                "message": "One or more interfaces are in a blocking STP state."
            })

    return issues
