# 🏟️ The Huddle

A **multi-sport fantasy assist platform** powered by **Vapi Squads** and **Qdrant**.

Users call a phone number, are greeted by the Huddle Host, pick their sport (Cricket, Football, or Chess), and get seamlessly handed off to a specialized sport guru that answers fantasy and stats questions by voice.

```
Voice Input → Vapi Squad → Huddle Host → Sport Guru → FastAPI → Qdrant → Voice Response
```

## Supported Sports

| Sport | Guru | Example Queries |
|-------|------|-----------------|
| 🏏 Cricket | Cricket Guru | "How did Kohli perform?" / "Who should I captain?" |
| ⚽ Football | Football Guru | "Is Haaland a good captain this week?" / "Tell me about Old Trafford" |
| ♟️ Chess | Chess Guru | "How good is Gukesh?" / "What opening should I learn?" |

## Project Structure

```
the-huddle/
├── app/
│   ├── main.py                      # FastAPI app with sport webhooks
│   ├── embeddings.py                # Deterministic embedding loader
│   └── sports/
│       ├── __init__.py              # Sport registry
│       ├── base_handler.py          # Base class for all sport handlers
│       ├── cricket/
│       │   ├── cricket_data.py      # Cricket match/player/venue data
│       │   ├── cricket_handler.py   # Qdrant queries for cricket
│       │   └── __init__.py
│       ├── football/
│       │   ├── football_data.py
│       │   ├── football_handler.py
│       │   └── __init__.py
│       └── chess/
│           ├── chess_data.py
│           ├── chess_handler.py
│           └── __init__.py
├── data/
│   ├── cricket_*.json               # Cricket embeddings
│   ├── football_*.json              # Football embeddings
│   └── chess_*.json                 # Chess embeddings
├── scripts/
│   ├── generate_embeddings.py       # Generate embeddings for any sport
│   └── setup_qdrant.py              # Create collections & load data
├── vapi-squad/
│   ├── squad-config.json            # Vapi Squad configuration template
│   ├── huddle-host-prompt.md
│   ├── cricket-guru-prompt.md
│   ├── football-guru-prompt.md
│   └── chess-guru-prompt.md
├── docker-compose.yml
└── requirements.txt
```

## Quick Start

### 1. Start Qdrant

```bash
docker start qdrant
# or if not created:
docker run -d -p 6333:6333 qdrant/qdrant
```

### 2. Set up Collections

```bash
cd the-huddle
python scripts/setup_qdrant.py
```

This creates all 12 collections (4 per sport) and loads the pre-computed embeddings.

### 3. Start the Backend

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Expose with ngrok

```bash
ngrok http 8000
```

Copy the `https` URL (e.g., `https://abc123.ngrok-free.app`).

### 5. Configure Vapi Squad

1. In the Vapi dashboard, create **4 assistants**:
   - **Huddle Host** — no server URL needed
   - **Cricket Guru** — server URL: `{ngrok-url}/vapi/webhook/cricket`
   - **Football Guru** — server URL: `{ngrok-url}/vapi/webhook/football`
   - **Chess Guru** — server URL: `{ngrok-url}/vapi/webhook/chess`

2. Copy the system prompts from `vapi-squad/*.md` into each assistant.

3. Add the same 5 functions to each guru:
   - `query_match_moment(query: string)`
   - `get_player_stats(player_name: string)`
   - `get_venue_insights(venue_name: string)`
   - `get_fantasy_advice(query: string)`
   - `general_sport_query(query: string)`

4. Add handoff tools so the Host can transfer to each guru, and each guru can transfer back to the Host.

5. Create a **Squad** in Vapi and add the 4 members. See `vapi-squad/squad-config.json` for the structure.

## Adding a New Sport

1. Create `app/sports/<sport>/<sport>_data.py` with the standard getters:
   - `get_all_moments()`, `get_all_players()`, `get_all_venues()`, `get_all_scenarios()`

2. Create `app/sports/<sport>/<sport>_handler.py` implementing `BaseSportHandler`.

3. Create `app/sports/<sport>/__init__.py` exporting the handler functions.

4. Generate embeddings:
   ```bash
   python scripts/generate_embeddings.py <sport>
   ```

5. Register the sport in `app/main.py` by adding the handler imports to `SPORT_HANDLERS`.

6. Re-run `python scripts/setup_qdrant.py`.

## Architecture Notes

- **Data-only pattern:** The backend returns raw JSON. Vapi's built-in LLM converts it into natural language.
- **Deterministic embeddings:** Uses hash-based embeddings (no PyTorch/OpenAI APIs needed).
- **Separate webhooks:** Each sport guru has its own endpoint for clean separation.

## Troubleshooting

**Qdrant connection error:** Make sure Docker is running at `localhost:6333`.

**Vapi not calling webhook:** Check that the ngrok URL is updated in the Vapi dashboard and includes the correct `/vapi/webhook/<sport>` path.

**Empty responses:** Run `python scripts/setup_qdrant.py` to ensure all collections are populated.
