import ipaddress


def check_ip_configuration(devices):
    issues = []

    ips = {}

    for device in devices:
        ip = device.get("ip")

        if not ip:
            continue

        try:
            ipaddress.ip_interface(ip)
        except ValueError:
            issues.append({
                "type": "invalid_ip",
                "device": device.get("name"),
                "message": f"Invalid IP address: {ip}"
            })
            continue

        if ip in ips:
            issues.append({
                "type": "duplicate_ip",
                "devices": [
                    ips[ip],
                    device.get("name")
                ],
                "message": f"Duplicate IP address detected: {ip}"
            })

        ips[ip] = device.get("name")

    return issues