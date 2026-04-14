# Pattern B: Data-Only Webhook

## Architecture

In this pattern, the webhook returns **raw data** from Qdrant, and **Vapi's GPT-5.4** generates the natural language response.

```
User Voice Query
    ↓
Vapi Speech-to-Text
    ↓
Vapi GPT-5.4 decides → "Call query_match_moment"
    ↓
POST /vapi/cricket-webhook
    ↓
Your Backend: Query Qdrant ONLY (no LLM)
    ↓
Return RAW DATA (JSON string)
    ↓
Vapi GPT-5.4 processes data + generates response
    ↓
Vapi Text-to-Speech
    ↓
User hears answer
```

## Webhook Response Format

```json
{
  "results": [{
    "toolCallId": "call_xxx",
    "result": "{\"player\": \"Tim David\", \"score\": \"70*\", \"sixes\": 8, ...}"
  }]
}
```

## Pros

- **Simpler webhook code** - Just database queries
- **Vapi LLM has full context** - Sees entire conversation + your data
- **Single system** - No external LLM dependency

## Cons

- **Less control** - Vapi decides how to phrase responses
- **May lose persona** - GPT-5.4 might not consistently sound like "CricVoice"
- **Higher cost** - Vapi charges for GPT-5.4 tokens
- **Slightly higher latency** - Two LLM calls (decide + generate)

## When to Use This Pattern

- When you want simpler backend code
- When Vapi's system prompt is sufficient for personality
- When cost is not a concern
- When you want Vapi to have full context awareness

## When NOT to Use

- When consistent brand voice is critical
- When you need specialized domain language (cricket terminology)
- When minimizing latency is important
- When operating on free tier budget
