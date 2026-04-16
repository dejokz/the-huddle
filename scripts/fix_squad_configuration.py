"""
Fix the entire Vapi Squad configuration:
- Clean Host handoff tools with proper names/descriptions
- Add 5 function tools to each Guru
- Add handoff-back-to-host tools to each Guru
- Set server URLs for all Gurus
- Fix Host firstMessage

Usage:
    python scripts/fix_squad_configuration.py
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

# IDs from your squad config
HOST_ID = "0cf2988e-e6d9-448b-a1a9-683a843a9084"
CRICKET_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
FOOTBALL_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
CHESS_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"
SQUAD_ID = "0b498751-5b9d-452e-b0c9-4defa99be921"

# Common function tool definitions for all sport gurus
FUNCTION_TOOLS = [
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "query_match_moment",
            "description": "Search for specific match events, moments, or highlights. Use when the user asks about a particular game moment, goal, wicket, brilliancy, or match event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language search query about the match moment"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_player_stats",
            "description": "Get statistics, ratings, and profile for a specific player. Use when the user asks about a named player or compares players.",
            "parameters": {
                "type": "object",
                "properties": {
                    "player_name": {
                        "type": "string",
                        "description": "The full name of the player"
                    }
                },
                "required": ["player_name"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_venue_insights",
            "description": "Get information about a stadium, ground, pitch, or strategy. Use when the user asks about venues, conditions, or opening strategies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "venue_name": {
                        "type": "string",
                        "description": "The name of the venue, stadium, or strategy"
                    }
                },
                "required": ["venue_name"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "get_fantasy_advice",
            "description": "Get fantasy league recommendations, captaincy picks, differentials, or fixture advice. Use when the user asks who to pick, captain, or bench.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The fantasy-related question or context"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "async": False,
        "function": {
            "name": "general_sport_query",
            "description": "Handle general sport-related questions that don't fit the other specific tools. Use for broad queries or when unsure which tool applies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The general sport question"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def update_assistant(assistant_id, name, payload):
    print(f"[PATCH] {name} ({assistant_id}) ...")
    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{assistant_id}",
        headers=HEADERS,
        json=payload,
    )
    if resp.status_code in [200, 201]:
        print(f"  [OK] {name} updated")
    else:
        print(f"  [ERROR] {name}: {resp.status_code}")
        print(f"  {resp.text}")
    return resp.status_code in [200, 201]


def fix_host():
    handoff_tools = [
        {
            "type": "handoff",
            "async": False,
            "function": {
                "name": "transfer_to_cricket_guru"
            },
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": CRICKET_ID,
                    "description": "Transfer to the Cricket Guru when the user wants cricket, IPL, or fantasy cricket help."
                }
            ]
        },
        {
            "type": "handoff",
            "async": False,
            "function": {
                "name": "transfer_to_football_guru"
            },
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": FOOTBALL_ID,
                    "description": "Transfer to the Football Guru when the user wants football, soccer, Premier League, or fantasy football help."
                }
            ]
        },
        {
            "type": "handoff",
            "async": False,
            "function": {
                "name": "transfer_to_chess_guru"
            },
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": CHESS_ID,
                    "description": "Transfer to the Chess Guru when the user wants chess, openings, grandmasters, or fantasy chess help."
                }
            ]
        }
    ]

    payload = {
        "firstMessage": "Hey there! Welcome to The Huddle — your personal fantasy assist hotline. Are you looking for help with cricket, football, or chess today?",
        "tools": handoff_tools,
    }
    return update_assistant(HOST_ID, "Huddle Host", payload)


def fix_guru(assistant_id, name, sport_path):
    handoff_back = {
        "type": "handoff",
        "async": False,
        "function": {
            "name": "transfer_back_to_host"
        },
        "destinations": [
            {
                "type": "assistant",
                "assistantId": HOST_ID,
                "description": "Transfer the user back to the Huddle Host when they want to switch sports or are done with their current question."
            }
        ]
    }

    tools = FUNCTION_TOOLS + [handoff_back]

    payload = {
        "serverUrl": f"{NGROK_URL}{sport_path}",
        "tools": tools,
        "firstMessage": None,  # Disable firstMessage since it's a handoff destination
    }
    return update_assistant(assistant_id, name, payload)


def fix_squad_overrides():
    """Clean up squad member overrides so Host doesn't have duplicate handoffs there."""
    print(f"[PATCH] Squad ({SQUAD_ID}) cleaning overrides ...")

    # Fetch current squad
    resp = requests.get(f"https://api.vapi.ai/squad/{SQUAD_ID}", headers=HEADERS)
    if resp.status_code != 200:
        print(f"  [ERROR] Could not fetch squad: {resp.status_code}")
        return False

    squad = resp.json()

    # Clean overrides: remove all assistantOverrides from members so tools live on assistants directly
    for member in squad.get("members", []):
        if "assistantOverrides" in member:
            del member["assistantOverrides"]

    update_resp = requests.patch(
        f"https://api.vapi.ai/squad/{SQUAD_ID}",
        headers=HEADERS,
        json={"members": squad["members"]},
    )

    if update_resp.status_code in [200, 201]:
        print("  [OK] Squad overrides cleaned")
    else:
        print(f"  [ERROR] Squad update failed: {update_resp.status_code}")
        print(f"  {update_resp.text}")
    return update_resp.status_code in [200, 201]


def main():
    ok = True
    ok &= fix_host()
    ok &= fix_guru(CRICKET_ID, "Cricket Guru", "/vapi/webhook/cricket")
    ok &= fix_guru(FOOTBALL_ID, "Football Guru", "/vapi/webhook/football")
    ok &= fix_guru(CHESS_ID, "Chess Guru", "/vapi/webhook/chess")
    ok &= fix_squad_overrides()

    if ok:
        print("\n[DONE] All squad configuration fixed!")
        print("\nQuick test checklist:")
        print("  1. Ensure ngrok is running on port 8001")
        print("  2. Ensure backend is running (docker-compose up or uvicorn)")
        print("  3. Make a test call to your squad")
        print("  4. Say 'cricket' -> should transfer to Cricket Guru")
        print("  5. Ask 'How did Virat Kohli perform?' -> should return stats")
    else:
        print("\n[WARN] Some updates failed. Check errors above.")


if __name__ == "__main__":
    main()
