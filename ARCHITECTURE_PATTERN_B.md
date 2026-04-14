# Pattern B: Data-Only Webhook (ACTIVE)

## How It Works

### The Flow

```
User: "Tell me about Tim David six"
         ↓
    [Vapi Speech-to-Text]
         ↓
    [Vapi GPT-5.4 + System Prompt]
    "User wants match info → call query_match_moment"
         ↓
    POST /vapi/cricket-webhook
    {
      "toolCalls": [{
        "function": {
          "name": "query_match_moment",
          "arguments": "{\"query\": \"Tim David six\"}"
        }
      }]
    }
         ↓
    [Your Backend - app/main.py]
    1. Query Qdrant for match data
    2. Return RAW DATA as JSON string:
    
    {
      "results": [{
        "toolCallId": "call_xxx",
        "result": "{\"player\": \"Tim David\", \"score\": \"70*\", \"balls\": 25, \"sixes\": 8, \"longest_six\": \"106m\", \"match\": \"RCB vs CSK\", \"venue\": \"Chinnaswamy\"}"
      }]
    }
         ↓
    [Vapi adds to conversation history]
    {
      "role": "tool",
      "content": "{\"player\": \"Tim David\", \"score\": \"70*\"...}"
    }
         ↓
    [Vapi GPT-5.4 reads data + System Prompt]
    System Prompt: "Use cricket terminology... sound enthusiastic..."
    
    GPT-5.4 generates:
    "Tim David was absolutely brutal! 70 not out off just 25 balls 
     with 8 sixes - including a 106-meter monster! That's death 
     overs carnage at its finest."
         ↓
    [Vapi ElevenLabs TTS]
         ↓
    🔊 "Tim David was absolutely brutal..."
```

## Key Components

### 1. System Prompt (Controls Description Style)

Located in: Vapi Dashboard → Assistant → Model → System Prompt

**What it tells Vapi:**
- Use cricket terminology: "carnage", "masterclass", "finisher"
- Sound enthusiastic like a commentator
- Reference specific stats from the data
- Never say "I don't have information"

**Example:**
```
When you receive data from tools, use that information to craft 
your response enthusiastically. If data shows: 
{"player": "Tim David", "sixes": 8}

Say: "Tim David unleashed carnage with 8 sixes!"
Don't say: "I found information about Tim David."
```

### 2. Webhook (Returns Raw Data)

**File:** `app/main.py`

**What it does:**
- Receives function calls from Vapi
- Queries Qdrant for data
- Returns JSON string (NOT generated text)

**Example return:**
```json
{
  "results": [{
    "toolCallId": "call_xxx",
    "result": "{\"player\": \"Tim David\", \"score\": \"70*\", \"balls\": 25}"
  }]
}
```

### 3. Vapi LLM (Generates Speech Text)

**Model:** GPT-5.4 (configured in Vapi dashboard)

**What it does:**
1. Decides which function to call (based on user query)
2. Receives JSON data from your webhook
3. Reads system prompt for style instructions
4. Generates natural language response
5. Sends to ElevenLabs for voice

## Why This Pattern?

### Advantages
1. **Simpler backend** - No LLM calls, just database queries
2. **Single system** - Vapi handles everything after data retrieval
3. **Full conversation context** - Vapi LLM sees entire conversation + your data
4. **Easy to modify tone** - Just update system prompt

### Trade-offs
1. **Cost** - Vapi GPT-5.4 charges per token
2. **Less control** - Vapi decides exact phrasing (though system prompt guides it)
3. **Latency** - Two LLM calls (decide + generate)

## Testing

1. Start server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

2. Start ngrok:
```bash
ngrok http 8000
```

3. Update webhook URL in Vapi assistant (if ngrok URL changed)

4. Call and ask: "Tell me about Tim David six"

5. Vapi should respond enthusiastically using cricket terminology!

## File Structure

```
starter-project/
├── app/
│   ├── main.py              ← Returns JSON data only
│   ├── cricket_data.py      ← Database query helpers
│   └── embeddings.py        ← Vector search
├── data/                    ← Qdrant vector data
└── update_vapi_prompt.py    ← Update system prompt
```

## System Prompt Key Instructions

The system prompt tells Vapi:

1. **Personality**: "Enthusiastic cricket analyst"
2. **Terminology**: "carnage", "masterclass", "finisher", "death overs"
3. **Data usage**: "Use the data, don't say you don't have information"
4. **Style**: "2-3 sentences, conversational like a commentator"

This ensures even though you're returning raw JSON, Vapi describes it with the "CricVoice" personality!
