# 🏏 CricVoice - Cricket Fantasy Agent

**CricVoice** is a voice-first cricket analyst bot that helps fantasy league players make informed decisions using match data from IPL 2026.

## What It Does

CricVoice can answer questions like:
- *"Who won the toss in RCB vs CSK?"*
- *"How did Virat Kohli perform?"*
- *"Who should I pick as captain - Kohli or Patidar?"*
- *"Tell me about Tim David's massive six"*
- *"How's the pitch at Chinnaswamy?"*

## Architecture

```
User Voice Query
    ↓
Vapi (Speech-to-Text)
    ↓
FastAPI Webhook (/vapi/cricket-webhook)
    ↓
Query Classification
    ├── match_moments (Qdrant)
    ├── player_context (Qdrant)
    ├── venue_insights (Qdrant)
    └── fantasy_scenarios (Qdrant)
    ↓
OpenAI LLM (Response Generation)
    ↓
Vapi (Text-to-Speech)
    ↓
User hears answer
```

## Data Sources

3 IPL 2026 matches with rich commentary:

| Match | Key Moments |
|-------|-------------|
| **RCB vs CSK** | Tim David's 70* (8 sixes, 106m onto roof), Sarfaraz Khan's fighting 50, Bhuvneshwar's 3 wickets |
| **RCB vs MI** | Hardik Pandya's wicket, Jacob Duffy bowling, Sherfane Rutherford sixes |
| **SRH vs RCB** | Jacob Duffy's dream debut (3 wickets), Kohli's 69* (first to 4000 chase runs!), Record 200+ chase in 15.4 overs |

## File Structure

```
app/
├── main.py                    # FastAPI app with webhooks
├── cricket_data.py            # Structured match data (12 moments, 8 players, 2 venues, 6 scenarios)
├── cricket_handler.py         # Query handler with Qdrant search
└── banking_handler.py         # (separate banking feature)

setup_cricket_qdrant.py        # Script to load data into Qdrant
CRICVOICE_README.md           # This file
```

## Qdrant Collections

| Collection | Items | Purpose |
|------------|-------|---------|
| `match_moments` | 12 | Ball-by-ball key events |
| `player_context` | 8 | Player stats and form |
| `venue_insights` | 2 | Ground characteristics |
| `fantasy_scenarios` | 6 | Captaincy/pick recommendations |

## Setup Instructions

### 1. Ensure Docker is running
```bash
docker-compose up
```

### 2. Add OpenAI API Key to .env
```bash
OPENAI_API_KEY=sk-your-real-key-here
VAPI_PRIVATE_KEY=your-vapi-key
BACKEND_URL=https://your-ngrok-url.ngrok-free.app
```

### 3. Load Cricket Data into Qdrant
```bash
python setup_cricket_qdrant.py
```

### 4. Start ngrok
```bash
ngrok http 8000
```

### 5. Configure Vapi Assistant
1. Go to https://dashboard.vapi.ai/assistants
2. Create new assistant
3. Get config: `curl http://localhost:8000/vapi/cricket-assistant-config`
4. Copy JSON to assistant settings
5. Set server URL to your ngrok URL + `/vapi/cricket-webhook`

### 6. Test
Call your Vapi number and ask:
- *"Tell me about the RCB vs CSK match"*
- *"How did Kohli perform?"*
- *"Who should I pick as captain?"*

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /vapi/cricket-webhook` | Main webhook for Vapi |
| `GET /vapi/cricket-assistant-config` | Assistant configuration JSON |
| `GET /health` | Health check with Qdrant status |

## Voice Functions Available

1. **query_match_moment** - Search specific match events
2. **get_player_stats** - Player statistics and history  
3. **get_venue_insights** - Ground/pitch information
4. **get_fantasy_advice** - Captaincy and pick recommendations
5. **general_cricket_query** - Handle any cricket question

## Player Profiles Available

- Virat Kohli (RCB) - S-tier, Chase master
- Tim David (RCB) - A-tier, Finisher
- Jacob Duffy (RCB) - A-tier, New ball specialist
- Rajat Patidar (RCB) - A-tier, Captain
- Sarfaraz Khan (CSK) - B-tier, Counter-attacker
- Bhuvneshwar Kumar (RCB) - A-tier, Swing bowler
- Devdutt Padikkal (RCB) - B-tier, Aggressive opener
- Hardik Pandya (MI) - A-tier, All-rounder

## Demo Script Ideas

### Demo 1: Match Moment
**User:** *"Tell me about Tim David's six"*
**Bot:** *"Oh, that was a monster! In the RCB vs CSK match at Chinnaswamy, Tim David unleashed absolute carnage. After getting a reprieve on a no-ball, he smashed a 106-meter six that landed on the stadium roof! He finished with 70 not out off just 25 balls with 8 sixes total. Fantasy gold for David owners!"*

### Demo 2: Player Stats
**User:** *"How's Virat Kohli performing?"*
**Bot:** *"Kohli is in excellent form! He's the first batter in IPL history to cross 4000 runs in successful chases. In the season opener against SRH, he scored an unbeaten 69 off 38 balls. At Chinnaswamy, his home ground, he averages a staggering 65 with 8 centuries. His recent scores are 69, 45, 85, 42, and 78 - consistently delivering for fantasy teams."*

### Demo 3: Fantasy Advice
**User:** *"Who should I pick as captain - Kohli or Patidar?"*
**Bot:** *"I'd go with Virat Kohli for captaincy. At Chinnaswamy, he averages 65 with 8 centuries - he's the chase master! While Patidar is in great form too and scored a quick 48 not out recently, Kohli's consistency and venue record make him the safer, high-reward pick. If you want a differential, Patidar as vice-captain could work."*

### Demo 4: Venue Info
**User:** *"How's the pitch at Chinnaswamy?"*
**Bot:** *"Chinnaswamy is a batting paradise! It's a high-scoring ground with an average first innings of 185. The boundaries are short at just 55-60 meters, perfect for six-hitters. The pitch has true bounce and the high altitude means the ball travels further. Dew factor helps the chasing team, which is why there's a 52% chase success rate here. Fantasy tip: pick power-hitters and chase masters!"*

## Tech Stack

- **Voice AI:** Vapi
- **Vector DB:** Qdrant
- **Backend:** FastAPI (Python)
- **Embeddings:** OpenAI text-embedding-3-small
- **LLM:** OpenAI GPT-3.5-turbo
- **Data:** Structured from Cricbuzz commentary

## Hackathon Track

**Track 1: Voice-First Knowledge & Workflow Agent**
- ✅ Retrieves and synthesizes cricket knowledge
- ✅ Assists in fantasy team decisions via voice
- ✅ Maintains context across queries
- ✅ Enables faster decision-making

## Notes

- Uses **simulated data** from real IPL 2026 matches
- Data extracted from Cricbuzz commentary pages
- All statistics and moments are factual
- Works 24/7 (no dependency on live matches)
- Demonstrates Vapi + Qdrant integration effectively

## Future Enhancements (Post-Hackathon)

- [ ] Live match API integration (CricAPI)
- [ ] Multi-language support (Hindi, Kannada)
- [ ] Push notifications for toss/playing XI
- [ ] Integration with Dream11/My11Circle APIs
- [ ] Historical data from previous IPL seasons

---

Built with ❤️ for cricket fans and fantasy league players!
