import pytest

from checker.ip_checker import check_ip_configuration
from checker.interface_checker import check_interfaces
from checker.vlan_checker import check_vlans
from checker.routing_checker import check_routes
from checker.checker import run_checks


# ============================================================
# IP CHECKER TESTS
# ============================================================

def test_ip_checker_valid_ips():
    devices = [
        {
            "name": "PC1",
            "ip": "192.168.1.10/24"
        },
        {
            "name": "PC2",
            "ip": "192.168.1.20/24"
        }
    ]

    result = check_ip_configuration(devices)

    assert result == []


def test_ip_checker_duplicate_ip():
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

    assert len(result) == 1
    assert result[0]["type"] == "duplicate_ip"
    assert "PC1" in result[0]["devices"]
    assert "PC2" in result[0]["devices"]


def test_ip_checker_invalid_ip():
    devices = [
        {
            "name": "PC1",
            "ip": "999.999.999.999/24"
        }
    ]

    result = check_ip_configuration(devices)

    assert len(result) == 1
    assert result[0]["type"] == "invalid_ip"


def test_ip_checker_missing_ip():
    devices = [
        {
            "name": "PC1"
        }
    ]

    result = check_ip_configuration(devices)

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


def test_interface_checker_interface_down():
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

    assert len(result) >= 1
    assert result[0]["type"] == "interface_down"


def test_interface_checker_administratively_down():
    commands = [
        {
            "command": "show ip interface brief",
            "output": """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/1      unassigned      YES unset administratively down   down
"""
        }
    ]

    result = check_interfaces(commands)

    assert len(result) >= 1
    assert result[0]["type"] == "interface_shutdown"


def test_interface_checker_irrelevant_command():
    commands = [
        {
            "command": "show version",
            "output": "Cisco IOS Software..."
        }
    ]

    result = check_interfaces(commands)

    assert result == []


# ============================================================
# VLAN CHECKER TESTS
# ============================================================

def test_vlan_checker_active_vlans():
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


def test_vlan_checker_no_active_vlans():
    commands = [
        {
            "command": "show vlan brief",
            "output": """
VLAN Name                             Status    Ports
"""
        }
    ]

    result = check_vlans(commands)

    assert len(result) >= 1
    assert result[0]["type"] == "missing_vlan"


def test_vlan_checker_irrelevant_command():
    commands = [
        {
            "command": "show ip route",
            "output": "Gateway of last resort is not set"
        }
    ]

    result = check_vlans(commands)

    assert result == []


# ============================================================
# ROUTING CHECKER TESTS
# ============================================================

def test_routing_checker_default_route_exists():
    commands = [
        {
            "command": "show ip route",
            "output": """
Gateway of last resort is 192.168.1.254 to network 0.0.0.0

C    192.168.1.0/24 is directly connected
S*   0.0.0.0/0 [1/0] via 192.168.1.254
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
C    192.168.2.0/24 is directly connected
"""
        }
    ]

    result = check_routes(commands)

    assert len(result) >= 1
    assert result[0]["type"] == "missing_default_route"


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
# COMBINATION TESTS
# ============================================================

def test_all_checkers_no_issues():
    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24"
            },
            {
                "name": "PC2",
                "ip": "192.168.1.20/24"
            }
        ],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
GigabitEthernet0/0 192.168.1.1 YES manual up up
"""
            },
            {
                "command": "show vlan brief",
                "output": """
10 SALES active
20 HR active
"""
            },
            {
                "command": "show ip route",
                "output": """
Gateway of last resort is 192.168.1.254
"""
            }
        ]
    }

    result = run_checks(data)

    assert result["issue_count"] == 0
    assert result["issues"] == []


def test_ip_and_interface_combination():
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
GigabitEthernet0/0 192.168.1.1 YES manual down down
"""
            }
        ]
    }

    result = run_checks(data)

    assert result["issue_count"] == 2

    issue_types = {
        issue["type"]
        for issue in result["issues"]
    }

    assert "duplicate_ip" in issue_types
    assert "interface_down" in issue_types


def test_interface_and_routing_combination():
    data = {
        "devices": [
            {
                "name": "PC1",
                "ip": "192.168.1.10/24"
            }
        ],

        "commands": [
            {
                "command": "show ip interface brief",
                "output": """
GigabitEthernet0/0 192.168.1.1 YES manual down down
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

    assert result["issue_count"] == 2

    issue_types = {
        issue["type"]
        for issue in result["issues"]
    }

    assert "interface_down" in issue_types
    assert "missing_default_route" in issue_types


def test_multiple_checkers_multiple_issues():
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
GigabitEthernet0/0 192.168.1.1 YES manual down down
"""
            },
            {
                "command": "show vlan brief",
                "output": """
VLAN Name Status Ports
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

    assert result["issue_count"] >= 4

    issue_types = {
        issue["type"]
        for issue in result["issues"]
    }

    assert "duplicate_ip" in issue_types
    assert "interface_down" in issue_types
    assert "missing_vlan" in issue_types
    assert "missing_default_route" in issue_types


# ============================================================
# EDGE CASE TESTS
# ============================================================

def test_empty_data():
    data = {}

    result = run_checks(data)

    assert result["issue_count"] == 0
    assert result["issues"] == []


def test_empty_devices_and_commands():
    data = {
        "devices": [],
        "commands": []
    }

    result = run_checks(data)

    assert result["issue_count"] == 0
    assert result["issues"] == []


def test_multiple_commands():
    commands = [
        {
            "command": "show ip interface brief",
            "output": """
GigabitEthernet0/0 192.168.1.1 YES manual up up
"""
        },
        {
            "command": "show vlan brief",
            "output": """
10 SALES active
"""
        },
        {
            "command": "show ip route",
            "output": """
Gateway of last resort is not set
"""
        }
    ]

    interface_result = check_interfaces(commands)
    vlan_result = check_vlans(commands)
    routing_result = check_routes(commands)

    assert interface_result == []
    assert vlan_result == []
    assert len(routing_result) == 1