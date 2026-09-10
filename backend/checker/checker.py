from checker.ip_checker import check_ip_configuration
from checker.interface_checker import check_interfaces
from checker.vlan_checker import check_vlans
from checker.routing_checker import check_routes
from checker.gateway_checker import check_gateways
from checker.dhcp_checker import check_dhcp
from checker.dns_checker import check_dns
from checker.acl_checker import check_acls
from checker.nat_checker import check_nat
from checker.trunk_checker import check_trunks
from checker.switchport_checker import check_switchports
from checker.stp_checker import check_stp
from checker.arp_checker import check_arp
from checker.connectivity_checker import check_connectivity


def run_checks(data):

    issues = []

    devices = data.get("devices", [])
    commands = data.get("commands", [])

    # 1. IP configuration
    issues.extend(check_ip_configuration(devices))

    # 2. Gateway
    issues.extend(check_gateways(devices))

    # 3. Interfaces
    issues.extend(check_interfaces(commands))

    # 4. VLAN
    issues.extend(check_vlans(commands))

    # 5. Routing
    issues.extend(check_routes(commands))

    # 6. DHCP
    issues.extend(check_dhcp(commands))

    # 7. DNS
    issues.extend(check_dns(commands))

    # 8. ACL
    issues.extend(check_acls(commands))

    # 9. NAT
    issues.extend(check_nat(commands))

    # 10. Trunk
    issues.extend(check_trunks(commands))

    # 11. Switchport
    issues.extend(check_switchports(commands))

    # 12. STP
    issues.extend(check_stp(commands))

    # 13. ARP
    issues.extend(check_arp(commands))

    # 14. Connectivity
    issues.extend(check_connectivity(commands))

    return {
        "issues": issues,
        "issue_count": len(issues)
    }