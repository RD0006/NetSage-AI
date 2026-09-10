def check_switchports(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "").lower()

        if "show interfaces switchport" not in command:
            continue

        for line in output.splitlines():

            if "administrative mode" in line:
                if "trunk" not in line and "access" not in line:
                    issues.append({
                        "type": "switchport_mode_invalid",
                        "message": "Switchport mode could not be determined."
                    })

    return issues