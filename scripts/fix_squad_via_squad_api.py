"""
Fix the Vapi Squad configuration for Bengaluru Sahayaka.
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

# IDs from your squad config
HOST_ID = "0cf2988e-e6d9-448b-a1a9-683a843a9084"
CERT_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
TAX_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
GRIEVANCE_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"

# Shared model config
MODEL_CONFIG = {
    "provider": "groq",
    "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
}

# Multilingual voice and transcriber overrides
HOST_VOICE = {
    "provider": "azure",
    "voiceId": "kn-IN-SapnaNeural",
}

GURU_VOICE = {
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

# Certificate Guru function tools
CERT_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "assess_eligibility",
            "description": "Determine the correct birth/death certificate procedural pathway based on citizen circumstances. Use when citizen asks about getting a new certificate, late registration, corrections, or duplicates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_type": {"type": "string", "description": "hospital or home"},
                    "days_since_birth": {"type": "integer", "description": "Number of days since birth"},
                    "request_type": {"type": "string", "description": "new, correction, duplicate, or name inclusion"},
                    "query": {"type": "string", "description": "The citizen's question or context"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "generate_document_checklist",
            "description": "Generate a personalized document checklist for certificate applications. Use after eligibility is determined or when citizen asks what documents to bring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "birth_type": {"type": "string", "description": "hospital or home"},
                    "days_since_birth": {"type": "integer", "description": "Number of days since birth"},
                    "request_type": {"type": "string", "description": "new, correction, duplicate, or name inclusion"},
                    "query": {"type": "string", "description": "The citizen's question or context"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_procedure_steps",
            "description": "Get step-by-step procedure guidance for certificate processes. Use when citizen asks how to apply, what are the steps, or what is the timeline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's question about procedures"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_affidavit_template",
            "description": "Provide spoken affidavit templates for corrections or late registration. Use when citizen needs help drafting an affidavit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "template_type": {"type": "string", "description": "Type of affidavit needed, e.g., minor correction, late registration, name inclusion"},
                    "query": {"type": "string", "description": "The citizen's question or context"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_office_info",
            "description": "Find BBMP zonal office information. Use when citizen asks where to go, office timings, or contact details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "zone_name": {"type": "string", "description": "The zone or area name in Bengaluru"},
                    "query": {"type": "string", "description": "The citizen's question about offices"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_cert_query",
            "description": "Handle general birth/death certificate questions that don't fit other specific tools. Use for broad queries or when unsure which tool applies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general certificate question"}
                },
                "required": ["query"]
            }
        }
    }
]

# Tax Guru function tools (Phase 1 scaffold)
TAX_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_tax_estimate",
            "description": "Provide basic property tax information. Use for simple tax queries in Phase 1.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's tax question"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_payment_options",
            "description": "Explain property tax payment options and deadlines. Use when citizen asks how or when to pay.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's payment question"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_tax_query",
            "description": "Handle general property tax questions. Use for broad tax queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general tax question"}
                },
                "required": ["query"]
            }
        }
    }
]

# Grievance Guru function tools (Phase 1 scaffold)
GRIEVANCE_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "file_complaint",
            "description": "Guide citizens on where to file complaints and which department handles their issue. Use for drainage, roads, streetlights, water, and building violations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The citizen's complaint or grievance"}
                },
                "required": ["query"]
            }
        }
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
                    "query": {"type": "string", "description": "The citizen's question about complaint status"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_grievance_query",
            "description": "Handle general grievance redressal questions. Use for broad grievance queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The general grievance question"}
                },
                "required": ["query"]
            }
        }
    }
]


def make_handoff_tool(name, dest_id, description, dest_overrides=None):
    destination = {
        "type": "assistant",
        "assistantId": dest_id,
        "description": description
    }
    if dest_overrides:
        destination["assistantOverrides"] = dest_overrides
    return {
        "type": "handoff",
        "async": False,
        "messages": [],
        "function": {"name": name},
        "destinations": [destination]
    }


def build_host_member():
    return {
        "assistantId": HOST_ID,
        "assistantOverrides": {
            "voice": HOST_VOICE,
            "transcriber": MULTILINGUAL_TRANSCRIBER,
            "firstMessage": "Namaskara! Welcome to Bengaluru Sahayaka. I can help you with birth certificates, property tax, and public grievances. English or Kannada — both are fine. What do you need help with today?",
            "model": {
                **MODEL_CONFIG,
                "messages": [
                    {
                        "role": "system",
                        "content": HOST_PROMPT
                    }
                ]
            },
            "tools:append": [
                make_handoff_tool(
                    "transfer_to_certificate_guru",
                    CERT_ID,
                    "Transfer to the Certificate Guru when the citizen asks about birth certificates, death certificates, corrections, duplicates, or name inclusion."
                ),
                make_handoff_tool(
                    "transfer_to_tax_guru",
                    TAX_ID,
                    "Transfer to the Tax Guru when the citizen asks about property tax, Khata, tax payment, or tax disputes."
                ),
                make_handoff_tool(
                    "transfer_to_grievance_guru",
                    GRIEVANCE_ID,
                    "Transfer to the Grievance Guru when the citizen has a complaint about roads, drainage, streetlights, water supply, building violations, or wants to file a public grievance."
                ),
            ]
        }
    }


def build_guru_member(assistant_id, name, service_path, greeting, prompt, tools):
    handoff_back = make_handoff_tool(
        "transfer_back_to_host",
        HOST_ID,
        "Transfer the citizen back to Bengaluru Sahayaka when they want a different service or are done with their current question.",
        dest_overrides={
            "firstMessage": "Welcome back to Bengaluru Sahayaka! Would you like help with another service, or is there anything else I can do for you?"
        }
    )
    return {
        "assistantId": assistant_id,
        "assistantOverrides": {
            "voice": GURU_VOICE,
            "transcriber": MULTILINGUAL_TRANSCRIBER,
            "serverUrl": f"{NGROK_URL}{service_path}",
            "firstMessage": greeting,
            "model": {
                **MODEL_CONFIG,
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    }
                ]
            },
            "tools:append": tools + [handoff_back]
        }
    }


def main():
    members = [
        build_host_member(),
        build_guru_member(
            CERT_ID,
            "certificate guru",
            "/vapi/webhook/certificates",
            "Hello! I'm your Certificate Assistant. I can guide you through birth and death certificate applications in Bengaluru. I can help in English or Kannada. What would you like to know?",
            CERT_PROMPT,
            CERT_TOOLS
        ),
        build_guru_member(
            TAX_ID,
            "tax guru",
            "/vapi/webhook/tax",
            "Hello! I'm your Tax Assistant. I can answer basic questions about BBMP property tax and Khata. I can help in English or Kannada. What would you like to know?",
            TAX_PROMPT,
            TAX_TOOLS
        ),
        build_guru_member(
            GRIEVANCE_ID,
            "grievance guru",
            "/vapi/webhook/grievances",
            "Hello! I'm your Grievance Assistant. I can help you understand where to file complaints about roads, drainage, streetlights, and other city issues. I can help in English or Kannada. What is your concern?",
            GRIEVANCE_PROMPT,
            GRIEVANCE_TOOLS
        ),
    ]

    payload = {
        "name": "Bengaluru Sahayaka",
        "members": members
    }

    print(f"[PATCH] Updating Squad {SQUAD_ID} ...")
    resp = requests.patch(
        f"https://api.vapi.ai/squad/{SQUAD_ID}",
        headers=HEADERS,
        json=payload,
    )

    if resp.status_code in [200, 201]:
        print("[OK] Squad updated successfully!")
        print("\nConfigured members:")
        member_names = [
            ("bengaluru sahayaka", HOST_ID),
            ("certificate guru", CERT_ID),
            ("tax guru", TAX_ID),
            ("grievance guru", GRIEVANCE_ID),
        ]
        for idx, (name, _) in enumerate(member_names):
            overrides = members[idx].get("assistantOverrides", {})
            tools = overrides.get("tools:append", [])
            server = overrides.get("serverUrl", "N/A")
            voice = overrides.get("voice", {})
            print(f"  - {name}: {len(tools)} tools, serverUrl={server}, voice={voice.get('voiceId')}")
        print("\nNext steps:")
        print("  1. Ensure ngrok is running on port 8001")
        print("  2. Ensure backend is running")
        print("  3. Test call your squad in English or Kannada!")
    else:
        print(f"[ERROR] {resp.status_code}")
        print(resp.text)


if __name__ == "__main__":
    main()
