import pytest

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

from checker.checker import run_checks


# ============================================================
# IP CHECKER TESTS
# ============================================================

def test_ip_checker_valid():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24"
        }
    ]

    result = check_ip_configuration(devices)

    assert result == []


def test_ip_checker_duplicate():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24"
        },
        {
            "name": "PC2",
            "ip": "192.168.1.10/24"
        }
    ]

    result = check_ip_configuration(devices)

    assert any(
        issue["type"] == "duplicate_ip"
        for issue in result
    )


def test_ip_checker_invalid():
    devices = [
        {
            "name": "PC1",
            "ip": "999.999.999.999/24"
        }
    ]

    result = check_ip_configuration(devices)

    assert any(
        issue["type"] == "invalid_ip"
        for issue in result
    )


def test_ip_checker_missing():
    devices = [
        {
            "name": "PC1"
        }
    ]

    result = check_ip_configuration(devices)

    assert result == []


# ============================================================
# GATEWAY CHECKER TESTS
# ============================================================

def test_gateway_checker_valid():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24",
            "gateway": "192.168.1.1"
        }
    ]

    result = check_gateways(devices)

    assert result == []


def test_gateway_checker_mismatch():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24",
            "gateway": "192.168.2.1"
        }
    ]

    result = check_gateways(devices)

    assert any(
        issue["type"] == "gateway_mismatch"
        for issue in result
    )


def test_gateway_checker_missing():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24"
        }
    ]

    result = check_gateways(devices)

    assert result == []


# ============================================================
# INTERFACE CHECKER TESTS
# ============================================================

def test_interface_checker_all_up():
    commands = [
        {
            "command": "show ip interface brief",
            "output": """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.1.1     YES manual up                    up
GigabitEthernet0/1      192.168.2.1     YES manual up                    up
"""
        }
    ]

    result = check_interfaces(commands)

    assert result == []


def test_interface_checker_down():
    commands = [
        {
            "command": "show ip interface brief",
            "output": """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.1.1     YES manual down                  down
"""
        }
    ]

    result = check_interfaces(commands)

    assert any(
        issue["type"] == "interface_down"
        for issue in result
    )


def test_interface_checker_administratively_down():
    commands = [
        {
            "command": "show ip interface brief",
            "output": """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.1.1     YES manual administratively down down
"""
        }
    ]

    result = check_interfaces(commands)

    assert any(
        issue["type"] == "interface_shutdown"
        for issue in result
    )


def test_interface_checker_irrelevant_command():
    commands = [
        {
            "command": "show version",
            "output": "Cisco IOS Software"
        }
    ]

    result = check_interfaces(commands)

    assert result == []


# ============================================================
# VLAN CHECKER TESTS
# ============================================================

def test_vlan_checker_active():
    commands = [
        {
            "command": "show vlan brief",
            "output": """
VLAN Name                             Status    Ports
1    default                          active    Fa0/1
10   SALES                            active    Fa0/2
20   HR                               active    Fa0/3
"""
        }
    ]

    result = check_vlans(commands)

    assert result == []


def test_vlan_checker_no_active_vlan():
    commands = [
        {
            "command": "show vlan brief",
            "output": """
VLAN Name                             Status    Ports
"""
        }
    ]

    result = check_vlans(commands)

    assert any(
        issue["type"] == "missing_vlan"
        for issue in result
    )


def test_vlan_checker_irrelevant_command():
    commands = [
        {
            "command": "show version",
            "output": "Cisco IOS Software"
        }
    ]

    result = check_vlans(commands)

    assert result == []


# ============================================================
# ROUTING CHECKER TESTS
# ============================================================

def test_routing_checker_default_route():
    commands = [
        {
            "command": "show ip route",
            "output": """
Gateway of last resort is 192.168.1.1 to network 0.0.0.0

C    192.168.1.0/24 is directly connected
S*   0.0.0.0/0 [1/0] via 192.168.1.1
"""
        }
    ]

    result = check_routes(commands)

    assert result == []


def test_routing_checker_missing_default_route():
    commands = [
        {
            "command": "show ip route",
            "output": """
Gateway of last resort is not set

C    192.168.1.0/24 is directly connected
"""
        }
    ]

    result = check_routes(commands)

    assert any(
        issue["type"] == "missing_default_route"
        for issue in result
    )


def test_routing_checker_irrelevant_command():
    commands = [
        {
            "command": "show vlan brief",
            "output": "10 SALES active"
        }
    ]

    result = check_routes(commands)

    assert result == []


# ============================================================
# DHCP CHECKER TESTS
# ============================================================

def test_dhcp_checker_valid():
    commands = [
        {
            "command": "show ip dhcp pool",
            "output": """
Pool DHCP_POOL :
 Utilization mark (high/low)    : 100 / 0
 Subnet size (first/next)       : 0 / 0
 Total addresses                : 254
 Leased addresses               : 10
 Network                        : 192.168.1.0 255.255.255.0
"""
        }
    ]

    result = check_dhcp(commands)

    assert result == []


def test_dhcp_checker_missing_pool():
    commands = [
        {
            "command": "show ip dhcp pool",
            "output": """
No DHCP pool configured
"""
        }
    ]

    result = check_dhcp(commands)

    assert any(
        issue["type"] == "dhcp_pool_missing"
        for issue in result
    )


def test_dhcp_checker_missing_network():
    commands = [
        {
            "command": "show ip dhcp pool",
            "output": """
Pool DHCP_POOL :
 Utilization mark (high/low) : 100 / 0
"""
        }
    ]

    result = check_dhcp(commands)

    assert any(
        issue["type"] == "dhcp_network_missing"
        for issue in result
    )


# ============================================================
# DNS CHECKER TESTS
# ============================================================

def test_dns_checker_configured():
    commands = [
        {
            "command": "show running-config",
            "output": """
hostname Router
ip name-server 8.8.8.8
"""
        }
    ]

    result = check_dns(commands)

    assert result == []


def test_dns_checker_missing():
    commands = [
        {
            "command": "show running-config",
            "output": """
hostname Router
interface GigabitEthernet0/0
"""
        }
    ]

    result = check_dns(commands)

    assert any(
        issue["type"] == "dns_missing"
        for issue in result
    )


# ============================================================
# ACL CHECKER TESTS
# ============================================================

def test_acl_checker_configured():
    commands = [
        {
            "command": "show access-lists",
            "output": """
Standard IP access list 10
    10 permit 192.168.1.0, wildcard bits 0.0.0.255
"""
        }
    ]

    result = check_acls(commands)

    assert result == []


def test_acl_checker_missing():
    commands = [
        {
            "command": "show access-lists",
            "output": ""
        }
    ]

    result = check_acls(commands)

    assert any(
        issue["type"] == "acl_missing"
        for issue in result
    )


# ============================================================
# NAT CHECKER TESTS
# ============================================================

def test_nat_checker_translation_exists():
    commands = [
        {
            "command": "show ip nat translations",
            "output": """
Pro  Inside global     Inside local       Outside local      Outside global
tcp  203.0.113.2:1025   192.168.1.10:1025 198.51.100.10:80 198.51.100.10:80
"""
        }
    ]

    result = check_nat(commands)

    assert result == []


def test_nat_checker_translation_missing():
    commands = [
        {
            "command": "show ip nat translations",
            "output": """
Pro  Inside global     Inside local       Outside local      Outside global
"""
        }
    ]

    result = check_nat(commands)

    assert any(
        issue["type"] == "nat_translation_missing"
        for issue in result
    )


# ============================================================
# TRUNK CHECKER TESTS
# ============================================================

def test_trunk_checker_exists():
    commands = [
        {
            "command": "show interfaces trunk",
            "output": """
Port        Mode         Encapsulation  Status        Native vlan
Gi0/1       on           802.1q         trunking      1
"""
        }
    ]

    result = check_trunks(commands)

    assert result == []


def test_trunk_checker_missing():
    commands = [
        {
            "command": "show interfaces trunk",
            "output": ""
        }
    ]

    result = check_trunks(commands)

    assert any(
        issue["type"] == "trunk_missing"
        for issue in result
    )


# ============================================================
# SWITCHPORT CHECKER TESTS
# ============================================================

def test_switchport_checker_valid():
    commands = [
        {
            "command": "show interfaces switchport",
            "output": """
Name: GigabitEthernet0/1
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
"""
        }
    ]

    result = check_switchports(commands)

    assert result == []


# ============================================================
# STP CHECKER TESTS
# ============================================================

def test_stp_checker_root_exists():
    commands = [
        {
            "command": "show spanning-tree",
            "output": """
VLAN0001
Spanning tree enabled protocol ieee
Root ID
    Priority 32769
    Address 0001.0001.0001

Port 1 Role Desg State FWD
"""
        }
    ]

    result = check_stp(commands)

    assert not any(
        issue["type"] == "stp_root_missing"
        for issue in result
    )


def test_stp_checker_blocking():
    commands = [
        {
            "command": "show spanning-tree",
            "output": """
VLAN0001
Spanning tree enabled protocol ieee
Root ID
    Priority 32769
    Address 0001.0001.0001

Port 1 Role Desg State FWD
Port 2 Role Altn State BLK
"""
        }
    ]

    result = check_stp(commands)

    assert any(
        issue["type"] == "stp_blocking"
        for issue in result
    )


# ============================================================
# ARP CHECKER TESTS
# ============================================================

def test_arp_checker_entries():
    commands = [
        {
            "command": "show ip arp",
            "output": """
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.1.10    0         0001.0001.0001  ARPA   GigabitEthernet0/0
"""
        }
    ]

    result = check_arp(commands)

    assert result == []


def test_arp_checker_empty():
    commands = [
        {
            "command": "show ip arp",
            "output": ""
        }
    ]

    result = check_arp(commands)

    assert any(
        issue["type"] == "arp_missing"
        for issue in result
    )


# ============================================================
# CONNECTIVITY CHECKER TESTS
# ============================================================

def test_connectivity_checker_success():
    commands = [
        {
            "command": "ping 192.168.1.1",
            "output": """
Success rate is 100 percent (5/5)
"""
        }
    ]

    result = check_connectivity(commands)

    assert result == []


def test_connectivity_checker_ping_failure():
    commands = [
        {
            "command": "ping 192.168.1.1",
            "output": """
Success rate is 0 percent (0/5)
"""
        }
    ]

    result = check_connectivity(commands)

    assert any(
        issue["type"] == "connectivity_failure"
        for issue in result
    )


def test_connectivity_checker_unreachable():
    commands = [
        {
            "command": "ping 192.168.1.1",
            "output": """
Destination host unreachable.
"""
        }
    ]

    result = check_connectivity(commands)

    assert any(
        issue["type"] == "host_unreachable"
        for issue in result
    )


# ============================================================
# COMBINATION TESTS
# ============================================================

def test_all_checkers_no_issues():

    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24",
                "gateway": "192.168.1.1"
            }
        ],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/0      192.168.1.1     YES manual up     up
"""
            },
            {
                "command": "show vlan brief",
                "output": """
10 SALES active Fa0/1
"""
            },
            {
                "command": "show ip route",
                "output": """
Gateway of last resort is 192.168.1.1
"""
            }
        ]
    }

    result = run_checks(data)

    assert isinstance(result, dict)
    assert "issues" in result
    assert "issue_count" in result


def test_combination_ip_and_interface():

    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24"
            },
            {
                "name": "PC2",
                "ip": "192.168.1.10/24"
            }
        ],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/1      192.168.1.2     YES manual down   down
"""
            }
        ]
    }

    result = run_checks(data)

    assert result["issue_count"] >= 2

    issue_types = [
        issue["type"]
        for issue in result["issues"]
    ]

    assert "duplicate_ip" in issue_types
    assert "interface_down" in issue_types


def test_combination_interface_and_routing():

    data = {
        "devices": [],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/1      192.168.1.2     YES manual down   down
"""
            },
            {
                "command": "show ip route",
                "output": """
Gateway of last resort is not set
"""
            }
        ]
    }

    result = run_checks(data)

    issue_types = [
        issue["type"]
        for issue in result["issues"]
    ]

    assert "interface_down" in issue_types
    assert "missing_default_route" in issue_types


def test_combination_gateway_and_ip():

    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24",
                "gateway": "192.168.2.1"
            },
            {
                "name": "PC2",
                "ip": "192.168.1.10/24",
                "gateway": "192.168.1.1"
            }
        ],

        "commands": []
    }

    result = run_checks(data)

    issue_types = [
        issue["type"]
        for issue in result["issues"]
    ]

    assert "duplicate_ip" in issue_types
    assert "gateway_mismatch" in issue_types


def test_multiple_issues():

    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24",
                "gateway": "192.168.2.1"
            }
        ],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/1      192.168.1.2     YES manual down   down
"""
            },
            {
                "command": "show ip route",
                "output": """
Gateway of last resort is not set
"""
            },
            {
                "command": "show spanning-tree",
                "output": """
VLAN0001
Port 2 Role Altn State BLK
"""
            }
        ]
    }

    result = run_checks(data)

    assert result["issue_count"] >= 3


# ============================================================
# EDGE CASE TESTS
# ============================================================

def test_run_checks_empty_data():

    data = {}

    result = run_checks(data)

    assert result["issues"] == []
    assert result["issue_count"] == 0


def test_run_checks_empty_devices_and_commands():

    data = {
        "devices": [],
        "commands": []
    }

    result = run_checks(data)

    assert result["issues"] == []
    assert result["issue_count"] == 0


def test_run_checks_multiple_commands():

    data = {
        "devices": [],

        "commands": [
            {
                "command": "show version",
                "output": "Cisco IOS"
            },
            {
                "command": "show vlan brief",
                "output": """
10 SALES active Fa0/1
"""
            },
            {
                "command": "show ip route",
                "output": """
Gateway of last resort is not set
"""
            }
        ]
    }

    result = run_checks(data)

    assert result["issue_count"] >= 1

    issue_types = [
        issue["type"]
        for issue in result["issues"]
    ]

    assert "missing_default_route" in issue_types
