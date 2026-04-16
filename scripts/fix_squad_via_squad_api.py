"""
Fix the Vapi Squad configuration by updating assistantOverrides on each member.
This is the correct API path for adding tools in a Squad.

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
CRICKET_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
FOOTBALL_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
CHESS_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"

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
        "function": {
            "name": name
        },
        "destinations": [destination]
    }


def build_host_member():
    return {
        "assistantId": HOST_ID,
        "assistantOverrides": {
            "voice": None,
            "transcriber": None,
            "firstMessage": "Hey there! Welcome to The Huddle — your personal fantasy assist hotline. Are you looking for help with cricket, football, or chess today?",
            "tools:append": [
                make_handoff_tool(
                    "transfer_to_cricket_guru",
                    CRICKET_ID,
                    "Transfer to the Cricket Guru when the user wants cricket, IPL, or fantasy cricket help."
                ),
                make_handoff_tool(
                    "transfer_to_football_guru",
                    FOOTBALL_ID,
                    "Transfer to the Football Guru when the user wants football, soccer, Premier League, or fantasy football help."
                ),
                make_handoff_tool(
                    "transfer_to_chess_guru",
                    CHESS_ID,
                    "Transfer to the Chess Guru when the user wants chess, openings, grandmasters, or fantasy chess help."
                ),
            ]
        }
    }


def build_guru_member(assistant_id, name, sport_path, greeting):
    handoff_back = make_handoff_tool(
        "transfer_back_to_host",
        HOST_ID,
        "Transfer the user back to the Huddle Host when they want to switch sports or are done with their current question.",
        dest_overrides={
            "firstMessage": "Welcome back to The Huddle! Ready to switch sports or is there anything else I can help you with?"
        }
    )
    return {
        "assistantId": assistant_id,
        "assistantOverrides": {
            "voice": None,
            "transcriber": None,
            "serverUrl": f"{NGROK_URL}{sport_path}",
            "firstMessage": greeting,
            "tools:append": FUNCTION_TOOLS + [handoff_back]
        }
    }


def main():
    members = [
        build_host_member(),
        build_guru_member(
            CRICKET_ID,
            "cricket guru",
            "/vapi/webhook/cricket",
            "Hey! I'm the Cricket Guru, your IPL fantasy specialist. What can I help you with today?"
        ),
        build_guru_member(
            FOOTBALL_ID,
            "football guru",
            "/vapi/webhook/football",
            "Hey! I'm the Football Guru, your Premier League fantasy specialist. What do you want to know?"
        ),
        build_guru_member(
            CHESS_ID,
            "chess guru",
            "/vapi/webhook/chess",
            "Hey! I'm the Chess Guru, your strategy and fantasy chess specialist. What's on your mind?"
        ),
    ]

    payload = {
        "name": "Huddle",
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
            ("huddle host", HOST_ID),
            ("cricket guru", CRICKET_ID),
            ("football guru", FOOTBALL_ID),
            ("chess guru", CHESS_ID),
        ]
        for idx, (name, _) in enumerate(member_names):
            overrides = members[idx].get("assistantOverrides", {})
            tools = overrides.get("tools:append", [])
            server = overrides.get("serverUrl", "N/A")
            voice = overrides.get("voice") or {}
            transcriber = overrides.get("transcriber") or {}
            print(f"  - {name}: {len(tools)} tools, serverUrl={server}, voice={voice.get('model')}, transcriber={transcriber.get('language')}")
        print("\nNext steps:")
        print("  1. Ensure ngrok is running on port 8001")
        print("  2. Ensure backend is running")
        print("  3. Test call your squad!")
    else:
        print(f"[ERROR] {resp.status_code}")
        print(resp.text)


if __name__ == "__main__":
    main()
