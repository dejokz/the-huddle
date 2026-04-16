# The Huddle - Project Handoff

## What This Application Does

The Huddle is a **multi-sport fantasy assist platform** powered by Vapi Squads. Users call a phone number, are greeted by the Huddle Host, pick a sport (Cricket, Football, or Chess), and get handed off to a specialized sport guru that answers fantasy and stats questions by voice.

### Supported Sports
- **Cricket** — IPL 2026 match moments, player stats, venue insights, fantasy advice
- **Football** — Premier League/Champions League moments, FPL-style player stats, stadium insights
- **Chess** — Famous games, GM profiles, opening strategy insights, fantasy chess advice

## System Architecture

The app uses a **Vapi Squad → Sport Guru → FastAPI → Qdrant** pattern:

1. User speaks to Vapi
2. The **Huddle Host** asks which sport
3. Host hands off to the appropriate **Sport Guru**
4. Sport Guru calls the backend webhook for that sport
5. FastAPI queries Qdrant and returns raw JSON
6. Vapi's LLM converts the JSON into natural language
7. Response is spoken back to the user

**Key decision:** Backend does NOT generate text. It only fetches data and returns JSON.

## Project Structure

```
the-huddle/
├── app/
│   ├── main.py                      # FastAPI app with sport webhooks
│   ├── embeddings.py                # Deterministic embedding loader
│   └── sports/
│       ├── __init__.py              # Sport registry
│       ├── base_handler.py          # Abstract base for sport handlers
│       ├── cricket/
│       │   ├── cricket_data.py
│       │   ├── cricket_handler.py
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
│   ├── cricket_*.json               # Cricket embeddings (12 items)
│   ├── football_*.json              # Football embeddings (28 items)
│   └── chess_*.json                 # Chess embeddings (23 items)
├── scripts/
│   ├── generate_embeddings.py       # Generate embeddings for any sport
│   └── setup_qdrant.py              # Create collections & load data
├── vapi-squad/
│   ├── squad-config.json            # Squad configuration template
│   ├── huddle-host-prompt.md
│   ├── cricket-guru-prompt.md
│   ├── football-guru-prompt.md
│   └── chess-guru-prompt.md
├── docker-compose.yml
└── requirements.txt
```

## Webhook Endpoints

Each sport has its own endpoint:
- `POST /vapi/webhook/cricket`
- `POST /vapi/webhook/football`
- `POST /vapi/webhook/chess`

Legacy endpoint (redirects to cricket):
- `POST /vapi/cricket-webhook`

## Sport Handler Pattern

All sport handlers implement `BaseSportHandler` with these methods:
- `query_match_moments(query: str) -> Dict`
- `query_player_stats(player_name: str, query: str = "") -> Dict`
- `query_venue_insights(venue_name: str) -> Dict`
- `query_fantasy_advice(query: str) -> Dict`
- `handle_general_query(query: str) -> Dict`

Return format:
```python
{
    "success": True/False,
    "response": "JSON string that will be sent to Vapi",
    "data": { ... }
}
```

## Qdrant Collections

| Sport | Collections |
|-------|-------------|
| Cricket | `cricket_match_moments`, `cricket_players`, `cricket_venues`, `cricket_fantasy_scenarios` |
| Football | `football_match_moments`, `football_players`, `football_venues`, `football_fantasy_scenarios` |
| Chess | `chess_match_moments`, `chess_players`, `chess_strategies`, `chess_fantasy_scenarios` |

**Setup:** Run `python scripts/setup_qdrant.py` to create all collections and load embeddings.

## Vapi Squad Configuration

The squad has 4 members:
1. **Huddle Host** — Greets, identifies sport, hands off
2. **Cricket Guru** — Server URL: `{ngrok}/vapi/webhook/cricket`
3. **Football Guru** — Server URL: `{ngrok}/vapi/webhook/football`
4. **Chess Guru** — Server URL: `{ngrok}/vapi/webhook/chess`

Each guru has the same 5 function definitions scoped to its sport. System prompts are in `vapi-squad/*.md`.

## Adding a New Sport

1. Create `app/sports/<sport>/<sport>_data.py` with getters:
   - `get_all_moments()`, `get_all_players()`, `get_all_venues()`, `get_all_scenarios()`
2. Create `app/sports/<sport>/<sport>_handler.py` implementing `BaseSportHandler`
3. Create `app/sports/<sport>/__init__.py`
4. Generate embeddings: `python scripts/generate_embeddings.py <sport>`
5. Register in `app/main.py` inside `_load_handlers()`
6. Re-run `python scripts/setup_qdrant.py`

## Running Locally

```bash
# 1. Start Qdrant
docker start qdrant

# 2. Setup collections
python scripts/setup_qdrant.py

# 3. Start backend
uvicorn app.main:app --reload --port 8000

# 4. Expose with ngrok
ngrok http 8000
```

## Common Issues

**Qdrant connection error:** Ensure Docker is running at `localhost:6333`

**Vapi webhook not reached:** Update ngrok URL in Vapi dashboard for each guru assistant

**Empty responses:** Run `setup_qdrant.py` — collections may be missing or empty

**Import errors:** Each sport `__init__.py` imports its handler, which requires `qdrant_client`. The backend must be run in an environment with all `requirements.txt` packages installed.
