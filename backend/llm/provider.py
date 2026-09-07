import os
import json
import re

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

Gemini_API_Key = os.getenv("Gemini_API_Key")

if not Gemini_API_Key:
    raise RuntimeError("Gemini_API_Key is not set in the environment.")


client = OpenAI(
    api_key=Gemini_API_Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


NETSAGE_SYSTEM_PROMPT = """
You are NetSage AI, a Cisco Packet Tracer network troubleshooting
advisor.

The deterministic Python checker is authoritative.

You MUST diagnose confirmed checker issues and MUST NOT replace them
with unrelated possible faults.

RULES:

1. If the checker reports an issue, that issue MUST be the basis of
   the diagnosis.

2. Never replace a confirmed issue with an unrelated issue.

3. Never invent:
   - IP addresses
   - interfaces
   - VLANs
   - routes
   - host-to-interface mappings
   - topology relationships

4. Never describe a confirmed checker issue as "possible" or "likely".

5. If the checker reports interface_shutdown:
   - root_cause must identify the affected interface as administratively
     down.
   - fault_domain must be "Interface".
   - confidence must be "High".
   - next_command should normally be [].
   - fix_steps should explain how to use "no shutdown" on the explicitly
     identified interface.

6. If the checker reports interface_down:
   diagnose the explicitly identified interface as down.

7. If the checker reports duplicate_ip:
   diagnose the duplicate IP address.

8. If the checker reports missing_vlan:
   diagnose the missing VLAN evidence.

9. If the checker reports missing_default_route:
   diagnose the missing default route.

10. If there is no confirmed checker issue, do not invent a fault.

11. If the evidence is insufficient:
   root_cause must be:
   "No deterministic root cause can be identified from the supplied evidence."

   fault_domain must be:
   "Undetermined"

   osi_layer must be:
   "Undetermined"

   fix_steps must be [].

12. Do not assume a host's physical switch port.

13. Do not use example interfaces unless explicitly present in the
    supplied evidence.

14. NetSage is suggest-only. It never executes commands or changes
    network devices.

Return ONLY valid JSON with exactly these fields:

{
    "root_cause": "string",
    "fault_domain": "string",
    "osi_layer": "string",
    "confidence": "High | Medium | Low",
    "evidence": ["string"],
    "next_command": ["string"],
    "fix_steps": ["string"]
}
"""


def _extract_json(response):
    """
    Extract JSON even if Gemini accidentally wraps it in ```json fences.
    """

    response = response.strip()

    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?", "", response, flags=re.IGNORECASE)
        response = re.sub(r"```$", "", response)
        response = response.strip()

    return json.loads(response)


def _build_authoritative_diagnosis(checker_result, commands, symptom):
    """
    Build a deterministic diagnosis for confirmed checker issues.

    This prevents the LLM from replacing an objective checker result
    with an unrelated hallucinated diagnosis.
    """

    issues = checker_result.get("issues", [])

    if not issues:
        return None

    evidence = []
    fix_steps = []
    root_cause = ""
    fault_domain = "Undetermined"
    osi_layer = "Undetermined"

    # --------------------------------------------------------
    # Interface administratively down
    # --------------------------------------------------------

    shutdown_issues = [
        issue for issue in issues
        if issue.get("type") == "interface_shutdown"
    ]

    if shutdown_issues:

        interfaces = [
            issue.get("interface")
            for issue in shutdown_issues
            if issue.get("interface")
        ]

        interface_text = ", ".join(interfaces)

        root_cause = (
            f"{interface_text} is administratively down."
        )

        fault_domain = "Interface"
        osi_layer = "Layer 1"

        for issue in shutdown_issues:
            interface = issue.get("interface", "Unknown interface")

            evidence.append(
                f"{interface} is administratively down."
            )

            evidence.append(
                f"{interface} has a down protocol status."
            )

            fix_steps.extend([
                f"Enter interface configuration mode for {interface}.",
                "Execute the no shutdown command.",
                f"Verify that {interface} is up/up."
            ])

    # --------------------------------------------------------
    # Interface down
    # --------------------------------------------------------

    down_issues = [
        issue for issue in issues
        if issue.get("type") == "interface_down"
    ]

    if down_issues and not shutdown_issues:

        interfaces = [
            issue.get("interface")
            for issue in down_issues
            if issue.get("interface")
        ]

        interface_text = ", ".join(interfaces)

        root_cause = (
            f"{interface_text} is down."
        )

        fault_domain = "Interface"
        osi_layer = "Layer 1"

        for issue in down_issues:
            interface = issue.get("interface", "Unknown interface")

            evidence.append(
                f"{interface} is down."
            )

            evidence.append(
                f"The supplied interface status indicates a connectivity problem."
            )

    # --------------------------------------------------------
    # Duplicate IP
    # --------------------------------------------------------

    duplicate_issues = [
        issue for issue in issues
        if issue.get("type") == "duplicate_ip"
    ]

    if duplicate_issues and not root_cause:

        issue = duplicate_issues[0]

        devices = issue.get("devices", [])
        ip = issue.get("message", "Duplicate IP address detected.")

        root_cause = ip
        fault_domain = "IP"
        osi_layer = "Layer 3"

        evidence.append(ip)

        if devices:
            evidence.append(
                f"The duplicate address is associated with: "
                f"{', '.join(str(d) for d in devices)}."
            )

        fix_steps = [
            "Assign unique IP addresses to the affected devices.",
            "Verify the IP configuration after correction."
        ]

    # --------------------------------------------------------
    # Missing VLAN
    # --------------------------------------------------------

    vlan_issues = [
        issue for issue in issues
        if issue.get("type") == "missing_vlan"
    ]

    if vlan_issues and not root_cause:

        root_cause = "No active VLANs were detected."

        fault_domain = "VLAN"
        osi_layer = "Layer 2"

        evidence.append(
            "The deterministic checker found no active VLANs."
        )

        fix_steps = [
            "Verify the VLAN configuration.",
            "Create or activate the required VLAN.",
            "Verify the VLAN using show vlan brief."
        ]

    # --------------------------------------------------------
    # Missing default route
    # --------------------------------------------------------

    route_issues = [
        issue for issue in issues
        if issue.get("type") == "missing_default_route"
    ]

    if route_issues and not root_cause:

        root_cause = "A default route is not configured."

        fault_domain = "Routing"
        osi_layer = "Layer 3"

        evidence.append(
            "The routing table reports that the gateway of last resort is not set."
        )

        fix_steps = [
            "Configure the required default route.",
            "Verify the routing table using show ip route."
        ]

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not root_cause:
        return None

    if len(evidence) < 3:
        evidence.append(
            f"The deterministic checker reported {len(issues)} confirmed issue(s)."
        )

    return {
        "root_cause": root_cause,
        "fault_domain": fault_domain,
        "osi_layer": osi_layer,
        "confidence": "High",
        "evidence": evidence[:5],
        "next_command": [],
        "fix_steps": fix_steps
    }


def generate_diagnosis(data, checker_result):

    symptom = data.get("symptom", "")
    devices = data.get("devices", [])
    connections = data.get("connections", [])
    commands = data.get("commands", [])
    notes = data.get("notes", "")

    # ========================================================
    # AUTHORITATIVE DETERMINISTIC DIAGNOSIS
    # ========================================================

    deterministic_diagnosis = _build_authoritative_diagnosis(
        checker_result,
        commands,
        symptom
    )

    if deterministic_diagnosis:
        return json.dumps(
            deterministic_diagnosis,
            indent=2
        )

    # ========================================================
    # LLM DIAGNOSIS ONLY WHEN NO CONFIRMED CHECKER ISSUE EXISTS
    # ========================================================

    user_prompt = f"""
SYMPTOM:
{symptom}

DEVICES:
{json.dumps(devices, indent=2)}

CONNECTIONS:
{json.dumps(connections, indent=2)}

TOPOLOGY NOTES:
{notes}

SHOW COMMAND OUTPUT:
{json.dumps(commands, indent=2)}

DETERMINISTIC CHECKER RESULT:
{json.dumps(checker_result, indent=2)}

No deterministic configuration fault was confirmed by the checker.

Analyze ONLY the supplied evidence.

If the evidence is insufficient to identify a root cause, use:

root_cause:
"No deterministic root cause can be identified from the supplied evidence."

fault_domain:
"Undetermined"

osi_layer:
"Undetermined"

fix_steps:
[]

Use next_command only for commands required to obtain missing evidence.

Return ONLY valid JSON.
"""

    completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": NETSAGE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    response = completion.choices[0].message.content

    if not response:
        raise RuntimeError("Gemini returned an empty response.")

    # Validate that Gemini actually returned JSON
    diagnosis = _extract_json(response)

    return json.dumps(
        diagnosis,
        indent=2
    )