# Pattern Comparison: CricVoice Architecture

## Quick Summary

| Aspect | Pattern A: Full LLM (`main`) | Pattern B: Data-Only (`feature/data-only`) |
|--------|------------------------------|--------------------------------------------|
| **LLM Used** | Groq Llama 4 Scout (free) | Vapi GPT-5.4 (paid) |
| **Response Generation** | Your backend | Vapi platform |
| **Control** | ✅ Full (consistent persona) | ⚠️ Limited (Vapi decides tone) |
| **Cost** | ✅ Free (Groq tier) | ❌ Per-token charges |
| **Latency** | ✅ Single LLM call | ❌ Two LLM calls |
| **Code Complexity** | Higher | Lower |
| **Conversation Context** | Limited | ✅ Full (Vapi sees everything) |

---

## Branch Structure

```
starter-project/
├── main (branch)
│   └── Pattern A: Full LLM Response Generation
│       └── app/main.py → Uses Groq Llama 4 to generate text
│
└── feature/data-only (branch)
    └── Pattern B: Data-Only Webhook
        └── app/main.py → Returns raw JSON for Vapi to process
```

---

## How to Switch Between Patterns

### Use Pattern A (Current - Full Control)
```bash
git checkout main
# Start server
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Use Pattern B (Simpler - Let Vapi Handle NLG)
```bash
git checkout feature/data-only
# Start server
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Note:** When using Pattern B, update Vapi's system prompt:
```
When you receive data from tools, respond like an enthusiastic 
cricket analyst using that data. Use cricket terminology naturally.
```

---

## Response Flow Comparison

### Pattern A: Your Backend Generates Text

```
User: "Tell me about Tim David six"
         ↓
    [Vapi GPT-5.4] → "Call query_match_moment"
         ↓
    POST to your webhook
         ↓
    [Your Backend]
    1. Query Qdrant → Get match data
    2. Send to Groq LLM
    3. Groq generates: "Tim David smashed a 106m six..."
         ↓
    Return: {"result": "Tim David smashed..."}
         ↓
    [Vapi speaks exactly what you returned]
```

**Result:** Consistent CricVoice personality every time.

---

### Pattern B: Vapi Generates Text from Your Data

```
User: "Tell me about Tim David six"
         ↓
    [Vapi GPT-5.4] → "Call query_match_moment"
         ↓
    POST to your webhook
         ↓
    [Your Backend]
    1. Query Qdrant → Get match data
    2. Format as JSON string
         ↓
    Return: {"result": "DATA: {player: 'Tim David', sixes: 8, ...}"}
         ↓
    [Vapi GPT-5.4 reads data]
    [Vapi GPT-5.4 generates response]
         ↓
    [Vapi speaks generated response]
```

**Result:** Vapi decides how to phrase it (may vary).

---

## Recommendation

**Use Pattern A (`main` branch)** for:
- Hackathon demos (consistent performance)
- Production with brand voice requirements
- Free tier operation

**Use Pattern B (`feature/data-only` branch)** for:
- Quick prototyping
- When conversation context > personality
- When you have budget for Vapi LLM

---

## Key Files by Pattern

| File | Pattern A | Pattern B |
|------|-----------|-----------|
| `app/main.py` | Full LLM orchestration | Data query only |
| `app/cricket_handler.py` | Used (Groq calls) | Not used |
| `app/cricket_data.py` | Backup source | Primary source |
| External LLM | Groq (free) | None (Vapi handles it) |

---

## Testing Both Patterns

```bash
# Terminal 1: Pattern A
git checkout main
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Pattern B
git checkout feature/data-only
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Compare the voice responses - Pattern A will be consistently "CricVoice", Pattern B will vary based on Vapi's interpretation.
