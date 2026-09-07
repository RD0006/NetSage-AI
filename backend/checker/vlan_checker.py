import re


def check_vlans(command_outputs):

    issues = []

    for item in command_outputs:

        command = item.get("command", "").lower()
        output = item.get("output", "")

        if "show vlan brief" not in command:
            continue

        vlan_ids = re.findall(
            r"^\s*(\d+)\s+\S+\s+active",
            output,
            re.MULTILINE
        )

        if not vlan_ids:
            issues.append({
                "type": "missing_vlan",
                "message": "No active VLANs were detected."
            })

    return issues