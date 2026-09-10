import ipaddress


def check_gateways(devices):
    issues = []

    for device in devices:
        ip = device.get("ip")
        gateway = device.get("gateway")

        if not ip or not gateway:
            continue

        try:
            interface = ipaddress.ip_interface(ip)
            gateway_ip = ipaddress.ip_address(gateway)

            if gateway_ip not in interface.network:
                issues.append({
                    "type": "gateway_mismatch",
                    "device": device.get("name"),
                    "message": (
                        f"Gateway {gateway} is not in the same subnet "
                        f"as {ip}."
                    )
                })

        except ValueError:
            continue

    return issues