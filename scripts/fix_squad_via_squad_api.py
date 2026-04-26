"""
Configure Bengaluru Sahayaka assistants directly, then attach them to the squad
without squad-level prompt overrides.

Usage:
    python scripts/fix_squad_via_squad_api.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not API_KEY:
    print("[ERROR] VAPI_PRIVATE_KEY not found")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

NGROK_URL = "https://ef5d-103-162-211-98.ngrok-free.app"
SQUAD_ID = "0b498751-5b9d-452e-b0c9-4defa99be921"

HOST_ID = "0cf2988e-e6d9-448b-a1a9-683a843a9084"
CERT_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
TAX_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
GRIEVANCE_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"

HOST_NAME = "Bengaluru Sahayaka Host"
CERT_NAME = "Birth & Death Certificates Assistant"
TAX_NAME = "Property Tax Assistant"
GRIEVANCE_NAME = "Public Grievance Assistant"

MODEL_CONFIG = {
    "provider": "groq",
    "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
}

HOST_VOICE = {
    "provider": "azure",
    "voiceId": "kn-IN-SapnaNeural",
}

SERVICE_VOICE = {
    "provider": "azure",
    "voiceId": "kn-IN-GaganNeural",
}

MULTILINGUAL_TRANSCRIBER = {
    "provider": "deepgram",
    "model": "nova-2-general",
    "language": "multi",
}


def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


HOST_PROMPT = load_prompt("vapi-squad/bengaluru-host-prompt.md")
CERT_PROMPT = load_prompt("vapi-squad/certificate-guru-prompt.md")
TAX_PROMPT = load_prompt("vapi-squad/tax-guru-prompt.md")
GRIEVANCE_PROMPT = load_prompt("vapi-squad/grievance-guru-prompt.md")


CERT_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "assess_eligibility",
            "description": "Determine the correct birth or death certificate procedural pathway based on citizen circumstances.",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_type": {"type": "string", "description": "hospital or home"},
                    "days_since_birth": {"type": "integer", "description": "Number of days since birth"},
                    "request_type": {"type": "string", "description": "new, correction, duplicate, or name inclusion"},
                    "query": {"type": "string", "description": "The citizen's question or context"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "generate_document_checklist",
            "description": "Generate a personalized document checklist for certificate applications.",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_type": {"type": "string", "description": "hospital or home"},
                    "days_since_birth": {"type": "integer", "description": "Number of days since birth"},
                    "request_type": {"type": "string", "description": "new, correction, duplicate, or name inclusion"},
                    "query": {"type": "string", "description": "The citizen's question or context"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_procedure_steps",
            "description": "Get step-by-step procedure guidance for certificate processes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's question about procedures"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_affidavit_template",
            "description": "Provide spoken affidavit templates for corrections or late registration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_type": {"type": "string", "description": "Type of affidavit needed"},
                    "query": {"type": "string", "description": "The citizen's question or context"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_office_info",
            "description": "Find BBMP zonal office information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_name": {"type": "string", "description": "The zone or area name in Bengaluru"},
                    "query": {"type": "string", "description": "The citizen's question about offices"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_cert_query",
            "description": "Handle general birth or death certificate questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general certificate question"},
                },
                "required": ["query"],
            },
        },
    },
]

TAX_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_tax_estimate",
            "description": "Provide basic property tax information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's tax question"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_payment_options",
            "description": "Explain property tax payment options and deadlines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's payment question"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_tax_query",
            "description": "Handle general property tax questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general tax question"},
                },
                "required": ["query"],
            },
        },
    },
]

GRIEVANCE_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "file_complaint",
            "description": "Guide citizens on where to file complaints and which department handles their issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's complaint or grievance"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_complaint_status",
            "description": "Explain how to check complaint status and escalation options.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's question about complaint status"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_grievance_query",
            "description": "Handle general grievance redressal questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general grievance question"},
                },
                "required": ["query"],
            },
        },
    },
]


def make_handoff_tool(name, dest_id, description):
    return {
        "type": "handoff",
        "async": False,
        "messages": [],
        "function": {"name": name},
        "destinations": [
            {
                "type": "assistant",
                "assistantId": dest_id,
                "description": description,
            }
        ],
    }


def update_assistant(assistant_id, label, payload):
    print(f"[PATCH] Assistant {label} ({assistant_id}) ...")
    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{assistant_id}",
        headers=HEADERS,
        json=payload,
    )
    if resp.status_code in [200, 201]:
        print(f"  [OK] {label} updated")
        return True

    print(f"  [ERROR] {label}: {resp.status_code}")
    print(resp.text)
    return False


def build_host_payload():
    return {
        "name": HOST_NAME,
        "voice": HOST_VOICE,
        "transcriber": MULTILINGUAL_TRANSCRIBER,
        "firstMessage": "Namaskara. This is Bengaluru Sahayaka. I can help with birth and death certificates, property tax, and public grievances. You can speak in English or Kannada. What do you need help with today?",
        "model": {
            **MODEL_CONFIG,
            "messages": [
                {
                    "role": "system",
                    "content": HOST_PROMPT,
                }
            ],
        },
    }


def build_service_payload(name, service_path, greeting, prompt, tools):
    return {
        "name": name,
        "voice": SERVICE_VOICE,
        "transcriber": MULTILINGUAL_TRANSCRIBER,
        "serverUrl": f"{NGROK_URL}{service_path}",
        "firstMessage": greeting,
        "model": {
            **MODEL_CONFIG,
            "messages": [
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
        },
    }


def build_squad_members():
    return [
        {
            "assistantId": HOST_ID,
            "assistantOverrides": {
                "tools:append": [
                    make_handoff_tool(
                        "transfer_to_birth_and_death_certificates_assistant",
                        CERT_ID,
                        "Transfer to the Birth & Death Certificates Assistant when the citizen asks about birth certificates, death certificates, corrections, duplicates, or name inclusion.",
                    ),
                    make_handoff_tool(
                        "transfer_to_property_tax_assistant",
                        TAX_ID,
                        "Transfer to the Property Tax Assistant when the citizen asks about property tax, Khata, tax payment, or tax disputes.",
                    ),
                    make_handoff_tool(
                        "transfer_to_public_grievance_assistant",
                        GRIEVANCE_ID,
                        "Transfer to the Public Grievance Assistant when the citizen has a complaint about roads, drainage, streetlights, water supply, building violations, or wants to file a public grievance.",
                    ),
                ]
            },
        },
        {
            "assistantId": CERT_ID,
            "assistantOverrides": {
                "tools:append": CERT_TOOLS
                + [
                    make_handoff_tool(
                        "transfer_back_to_bengaluru_sahayaka_host",
                        HOST_ID,
                        "Transfer the citizen back to the Bengaluru Sahayaka Host when they want a different service or are done with their current question.",
                    )
                ]
            },
        },
        {
            "assistantId": TAX_ID,
            "assistantOverrides": {
                "tools:append": TAX_TOOLS
                + [
                    make_handoff_tool(
                        "transfer_back_to_bengaluru_sahayaka_host",
                        HOST_ID,
                        "Transfer the citizen back to the Bengaluru Sahayaka Host when they want a different service or are done with their current question.",
                    )
                ]
            },
        },
        {
            "assistantId": GRIEVANCE_ID,
            "assistantOverrides": {
                "tools:append": GRIEVANCE_TOOLS
                + [
                    make_handoff_tool(
                        "transfer_back_to_bengaluru_sahayaka_host",
                        HOST_ID,
                        "Transfer the citizen back to the Bengaluru Sahayaka Host when they want a different service or are done with their current question.",
                    )
                ]
            },
        },
    ]


def main():
    ok = True
    ok &= update_assistant(HOST_ID, HOST_NAME, build_host_payload())
    ok &= update_assistant(
        CERT_ID,
        CERT_NAME,
        build_service_payload(
            CERT_NAME,
            "/vapi/webhook/certificates",
            "Hello. You have reached the Birth and Death Certificates Assistant. I can help with registrations, corrections, duplicate certificates, and document requirements in Bengaluru. What would you like help with?",
            CERT_PROMPT,
            CERT_TOOLS,
        ),
    )
    ok &= update_assistant(
        TAX_ID,
        TAX_NAME,
        build_service_payload(
            TAX_NAME,
            "/vapi/webhook/tax",
            "Hello. You have reached the Property Tax Assistant. I can help with BBMP property tax, Khata questions, payments, and basic disputes. What would you like help with?",
            TAX_PROMPT,
            TAX_TOOLS,
        ),
    )
    ok &= update_assistant(
        GRIEVANCE_ID,
        GRIEVANCE_NAME,
        build_service_payload(
            GRIEVANCE_NAME,
            "/vapi/webhook/grievances",
            "Hello. You have reached the Public Grievance Assistant. I can help you understand where to file civic complaints and how to follow up on them in Bengaluru. What is the issue you are facing?",
            GRIEVANCE_PROMPT,
            GRIEVANCE_TOOLS,
        ),
    )

    payload = {
        "name": "Bengaluru Sahayaka",
        "members": build_squad_members(),
    }

    print(f"[PATCH] Updating Squad {SQUAD_ID} with clean member references ...")
    resp = requests.patch(
        f"https://api.vapi.ai/squad/{SQUAD_ID}",
        headers=HEADERS,
        json=payload,
    )

    ok &= resp.status_code in [200, 201]

    if resp.status_code in [200, 201]:
        print("[OK] Squad updated successfully!")
        print("\nConfigured members:")
        print(f"  - {HOST_NAME}: 3 handoff tools")
        print(f"  - {CERT_NAME}: {len(CERT_TOOLS) + 1} tools, serverUrl={NGROK_URL}/vapi/webhook/certificates")
        print(f"  - {TAX_NAME}: {len(TAX_TOOLS) + 1} tools, serverUrl={NGROK_URL}/vapi/webhook/tax")
        print(f"  - {GRIEVANCE_NAME}: {len(GRIEVANCE_TOOLS) + 1} tools, serverUrl={NGROK_URL}/vapi/webhook/grievances")
    else:
        print(f"[ERROR] {resp.status_code}")
        print(resp.text)

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
