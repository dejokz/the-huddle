"""
Update Vapi Squad greetings and host welcome-back behavior.
- Gurus get useful firstMessages instead of generic "Hi."
- Host prompt updated to say "welcome back" on return handoffs.

Usage:
    python scripts/update_squad_greetings.py
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
CRICKET_ID = "ec398ab7-64e2-47f6-abe7-f4752ca51b9e"
FOOTBALL_ID = "a4696f51-15e8-4556-aa7e-3901edb806dd"
CHESS_ID = "fd34e6be-5a44-4a15-b1a4-4b1f39fc7d0f"

HOST_PROMPT = """# Huddle Host - System Prompt

You are the **Huddle Host**, the warm and enthusiastic greeting assistant for The Huddle — a multi-sport fantasy assist platform.

## Your Job
1. **Greet the caller** warmly and briefly.
2. **Ask which sport** they want help with: Cricket, Football, or Chess.
3. **Confirm their choice** and then use the appropriate handoff tool to transfer them to the right sport guru.

## Personality
- Energetic, friendly, and concise.
- Sports-curious — you sound like someone who loves all games.
- Never try to answer sport-specific questions yourself.

## Handoff Rules
- If the user says "cricket" → transfer to **Cricket Guru**
- If the user says "football" or "soccer" → transfer to **Football Guru**
- If the user says "chess" → transfer to **Chess Guru**
- If the user is unsure, briefly describe each option (1 sentence each) and ask again.
- If the user wants to switch sports mid-conversation, transfer them back to the Host (this happens automatically via squad tools).

## Welcome Back Behavior
**CRITICAL:** If the user is returning to you after talking to a Cricket Guru, Football Guru, or Chess Guru, do NOT repeat your initial introduction.

Instead, say something warm and brief like:
> "Welcome back! Want to explore another sport, or is there something else I can help you with?"

## Example Dialogue (First Call)
> "Hey there! Welcome to The Huddle — your personal fantasy assist hotline. Are you looking for help with cricket, football, or chess today?"

> "Cricket it is! Let me connect you with our Cricket Guru. One sec!"

## Example Dialogue (Return from Guru)
> "Welcome back! Ready to dive into another sport, or are you all set?"

**CRITICAL:** Do NOT answer stats or fantasy questions. Your only job is routing.
"""


def make_handoff_tool(name, dest_id, description):
    return {
        "type": "handoff",
        "async": False,
        "messages": [],
        "function": {
            "name": name
        },
        "destinations": [
            {
                "type": "assistant",
                "assistantId": dest_id,
                "description": description
            }
        ]
    }


def main():
    members = [
        {
            "assistantId": HOST_ID,
            "assistantOverrides": {
                "firstMessage": "Hey there! Welcome to The Huddle — your personal fantasy assist hotline. Are you looking for help with cricket, football, or chess today?",
                "model": {
                    "provider": "groq",
                    "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": HOST_PROMPT
                        }
                    ]
                },
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
        },
        {
            "assistantId": CRICKET_ID,
            "assistantOverrides": {
                "firstMessage": "Hey! I'm the Cricket Guru, your IPL fantasy specialist. What can I help you with today?",
                "serverUrl": f"{NGROK_URL}/vapi/webhook/cricket"
            }
        },
        {
            "assistantId": FOOTBALL_ID,
            "assistantOverrides": {
                "firstMessage": "Hey! I'm the Football Guru, your Premier League fantasy specialist. What do you want to know?",
                "serverUrl": f"{NGROK_URL}/vapi/webhook/football"
            }
        },
        {
            "assistantId": CHESS_ID,
            "assistantOverrides": {
                "firstMessage": "Hey! I'm the Chess Guru, your strategy and fantasy chess specialist. What's on your mind?",
                "serverUrl": f"{NGROK_URL}/vapi/webhook/chess"
            }
        },
    ]

    payload = {
        "name": "Huddle",
        "members": members
    }

    print(f"[PATCH] Updating Squad {SQUAD_ID} greetings ...")
    resp = requests.patch(
        f"https://api.vapi.ai/squad/{SQUAD_ID}",
        headers=HEADERS,
        json=payload,
    )

    if resp.status_code in [200, 201]:
        print("[OK] Squad greetings updated successfully!")
        print("\nChanges applied:")
        print("  - Huddle Host: welcome-back behavior added")
        print("  - Cricket Guru: 'Hey! I'm the Cricket Guru...'")
        print("  - Football Guru: 'Hey! I'm the Football Guru...'")
        print("  - Chess Guru: 'Hey! I'm the Chess Guru...'")
    else:
        print(f"[ERROR] {resp.status_code}")
        print(resp.text)


if __name__ == "__main__":
    main()
