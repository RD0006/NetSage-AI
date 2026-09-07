from checker.ip_checker import check_ip_configuration
from checker.interface_checker import check_interfaces
from checker.vlan_checker import check_vlans
from checker.routing_checker import check_routes


def run_checks(data):

    issues = []

    devices = data.get("devices", [])
    commands = data.get("commands", [])

    # 1. IP checks
    issues.extend(
        check_ip_configuration(devices)
    )

    # 2. Interface checks
    issues.extend(
        check_interfaces(commands)
    )

    # 3. VLAN checks
    issues.extend(
        check_vlans(commands)
    )

    # 4. Routing checks
    issues.extend(
        check_routes(commands)
    )

    return {
        "issues": issues,
        "issue_count": len(issues)
    }