    """
Add handoff tools to the Huddle Host assistant via Vapi API.
Usage:
    python scripts/setup_huddle_host_tools.py <HOST_ASSISTANT_ID> [CRICKET_ID] [FOOTBALL_ID] [CHESS_ID]

If destination IDs are omitted, placeholders will be used and you'll need to update them later.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_PRIVATE_KEY")
if not API_KEY:
    print("[ERROR] VAPI_PRIVATE_KEY not found in environment or .env")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/setup_huddle_host_tools.py <HOST_ASSISTANT_ID> [CRICKET_ID] [FOOTBALL_ID] [CHESS_ID]")
        sys.exit(1)

    host_id = sys.argv[1]
    cricket_id = sys.argv[2] if len(sys.argv) > 2 else "<CRICKET_ASSISTANT_ID>"
    football_id = sys.argv[3] if len(sys.argv) > 3 else "<FOOTBALL_ASSISTANT_ID>"
    chess_id = sys.argv[4] if len(sys.argv) > 4 else "<CHESS_ASSISTANT_ID>"

    handoff_tools = [
        {
            "type": "handoff",
            "name": "transferToCricketGuru",
            "description": "Transfer the caller to the Cricket Guru when they express interest in cricket, IPL, or fantasy cricket help.",
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": cricket_id,
                }
            ],
        },
        {
            "type": "handoff",
            "name": "transferToFootballGuru",
            "description": "Transfer the caller to the Football Guru when they express interest in football, soccer, Premier League, or fantasy football help.",
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": football_id,
                }
            ],
        },
        {
            "type": "handoff",
            "name": "transferToChessGuru",
            "description": "Transfer the caller to the Chess Guru when they express interest in chess, openings, grandmasters, or fantasy chess help.",
            "destinations": [
                {
                    "type": "assistant",
                    "assistantId": chess_id,
                }
            ],
        },
    ]

    # We use 'tools:append' via assistantOverrides pattern or directly patch the assistant.
    # Patching the assistant directly with the tools array.
    update_data = {
        "tools": handoff_tools,
    }

    print(f"[SETUP] Adding handoff tools to Huddle Host ({host_id}) ...")
    resp = requests.patch(
        f"https://api.vapi.ai/assistant/{host_id}",
        headers=HEADERS,
        json=update_data,
    )

    if resp.status_code in [200, 201]:
        print("[OK] Handoff tools added successfully!")
        for tool in handoff_tools:
            dest_id = tool["destinations"][0]["assistantId"]
            print(f"  - {tool['name']} -> {dest_id}")
    else:
        print(f"[ERROR] {resp.status_code}")
        print(resp.text)


if __name__ == "__main__":
    main()
