# NetSage AI

### AI-Assisted Network Troubleshooting with Human Review

Author: Radhika Diwan

NetSage AI is an AI-assisted network troubleshooting application designed to help users diagnose common Cisco Packet Tracer networking problems.

The system combines **deterministic Python-based network checks** with a **Gemini Large Language Model (LLM)** to analyze network symptoms, topology information, Cisco command outputs, and additional notes.

A key feature of NetSage AI is its **Human-in-the-Loop** approach. AI-generated diagnoses are not automatically accepted or applied. A human reviewer must review the diagnosis before it is considered final.


## Features

- Network symptom analysis
- Dynamic network topology input
- Cisco `show` command output analysis
- Deterministic rule-based network checking
- AI-assisted troubleshooting using Gemini
- Structured JSON diagnosis
- Root cause identification
- Fault domain identification
- OSI layer identification
- Confidence and severity levels
- Evidence-based troubleshooting
- Suggested next commands
- Recommended fix steps
- Human review:
  - Accepted
  - Edited
  - Rejected
- Analysis history using browser local storage
- Working and faulty Packet Tracer test scenarios

## System Architecture

```text
                User
                  |
                  v
          React Frontend
                  |
       Symptom + Topology +
       Command Outputs + Notes
                  |
                  v
           Flask Backend
                  |
                  v
       Input Validation
                  |
                  v
      Deterministic Checker
          /             \
         /               \
 Confirmed Fault       No Confirmed Fault
       |                    |
       v                    v
 Deterministic          Gemini LLM
   Evidence               Analysis
       \                    /
        \                  /
         v                v
             Diagnosis
                 |
                 v
          Human Review
                 |
       +---------+---------+
       |         |         |
    Accepted   Edited   Rejected
```

## Technology Stack
- Frontend
    - React.js
    - Vite
    - Tailwind CSS
    - Browser Local Storage
- Backend
    - Python
    - Flask
    - Pydantic
    - Flask-CORS
- AI
    - Google Gemini LLM
    - Structured JSON output
    - Evidence-based prompting
- Networking
    - Cisco Packet Tracer
    - Cisco IOS show commands
- Testing
    - Pytest


## How It Works
1. User Provides Network Information
```text
  The user enters:

  - Network symptom
  - Devices and IP addresses
  - Network connections
  - Cisco command outputs
  - Additional notes

  Example:

  {
    "symptom": "PC1 is unable to reach the server.",
    "devices": [
      {
        "name": "PC1",
        "ip": "192.168.1.10/24"
      },
      {
        "name": "Router1",
        "ip": "192.168.1.1/24"
      },
      {
        "name": "Router2",
        "ip": "10.0.0.2/30"
      },
      {
        "name": "Server",
        "ip": "192.168.10.10/24"
      }
    ]
  }
```

2. Deterministic Network Checks

```text
  Before relying on the LLM, the backend performs rule-based checks on the supplied evidence.

  The implemented checks include:
  • ACL Checker  
  • ARP Checker  
  • Connectivity Checker  
  • DHCP Checker  
  • DNS Checker  
  • Gateway Checker  
  • Interface Checker  
  • IP Checker  
  • NAT Checker  
  • Port Security Checker  
  • Routing Checker  
  • STP Checker  
  • Switchport Checker  
  • Trunk Checker  
  • VLAN Checker

  These checks provide deterministic evidence that can be supplied to the AI.
```

3. AI Diagnosis
```text
  When additional reasoning is required, the supplied evidence is passed to Gemini.

  The AI produces a structured diagnosis containing:

  {
    "root_cause": "string",
    "fault_domain": "string",
    "osi_layer": "string",
    "confidence": "High | Medium | Low",
    "severity": "Critical | High | Medium | Low",
    "evidence": [],
    "next_command": [],
    "fix_steps": []
  }

  The AI is instructed to reason only from the supplied evidence and avoid inventing network information.
```

4. Human Review
```text
  Every diagnosis requires human review.

  The reviewer can:

  • Accept the diagnosis if it is correct.
  • Edit the diagnosis if changes are required.
  • Reject the diagnosis if it is incorrect or unsupported.

  This prevents the AI from acting as an autonomous network administrator.

  Example Diagnosis

  - Input

  • Problem: PC1 is unable to reach the server.

  • Topology: 
    PC1
    |
    Router1
    |
    Router2
    |
    Server

  • The routing table does not contain a route to: 192.168.10.0/24


  - NetSage AI Diagnosis

  • Likely Fault: The router lacks a route to destination network 192.168.10.0/24.

  • Confidence: High

  • Severity: High

  • OSI Layer: Layer 3

  • Fault Domain: Routing

  The system provides the supporting evidence and recommends configuring the appropriate route and verifying connectivity.

  The human reviewer can then accept, edit, or reject the diagnosis.
```

## Project Structure

```text
NetSage-AI/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── checker/
│   │   ├── checker.py
│   │   ├── ip_checker.py
│   │   ├── interface_checker.py
│   │   ├── vlan_checker.py
│   │   └── routing_checker.py
│   │
│   ├── llm/
│   │   └── provider.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── app.py
│   ├── requirements.txt
│   └── ...
│
├── dataset/
│   └── cases.csv
│
├── prompts/
│   └── diagnose_prompt.md
│
├── tests/
│   └── ...
│
└── README.md
```

The exact structure may vary depending on the final repository organization.

## Testing

NetSage AI includes automated tests for the deterministic network checker and backend functionality.

The project includes tests cover the following among many other tests:

- IP validation
- Duplicate IP detection
- Interface status
- VLAN checks
- Routing checks
- Normal/no-fault cases
- Invalid input
- Backend integration

## Test Case

The project was also tested using Cisco Packet Tracer scenarios.

Test Case — Missing Route
PC1 ─── Router1 ─── Router2 ─── Server

Fault:

Router1 does not have a route
to 192.168.10.0/24

NetSage AI identifies the routing problem using the supplied show ip route output.

Responsible AI Approach

NetSage AI follows several principles to make AI-assisted troubleshooting safer:

Evidence-based reasoning
The AI should use only information supplied by the user and deterministic checker.
No invented configuration
The system discourages the AI from creating unsupported network facts.
Deterministic validation
Rule-based checks provide objective evidence where possible.
Human review
AI diagnoses require human approval before being considered final.
No automatic remediation
NetSage AI recommends troubleshooting actions but does not automatically modify network devices.
## Limitations
- The application does not directly read Cisco Packet Tracer .pkt files.
- Diagnosis depends on the quality of supplied command output and topology information.
- Deterministic checker coverage is limited to the implemented checks.

## Future Improvements

Possible future improvements include the following:
- Direct .pkt file analysis
- Additional Cisco command checkers
- Expanded DHCP, DNS, ACL, NAT, wireless, STP, and trunk analysis
- Automatic extraction of Packet Tracer topology information
- More extensive network datasets
- Improved AI evaluation metrics
- Persistent database-based troubleshooting history
- Network device integration for controlled verification


## Project Objective

The objective of NetSage AI is not to replace network engineers. Instead, it demonstrates how deterministic network validation, Large Language Models, structured outputs, and human review can be combined to assist with network troubleshooting while keeping a human responsible for the final decision.
