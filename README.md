# 🎙️ Voice Memory Starter

A minimal project to experiment with **Vapi** (voice AI) + **Qdrant** (vector database).

## What This Does

```
Voice Input → Vapi → Your Backend → Qdrant → Semantic Search → Voice Response
```

**Use it like:**
- *"Remember that my Docker container crashes with exit code 137"* → Stored in Qdrant
- *"Why is my container failing?"* → Finds & speaks back your memory

## 🚀 Quick Start

### 1. Prerequisites

- Docker & Docker Compose
- OpenAI API key
- (Optional) Vapi account for voice testing

### 2. Setup Environment

```bash
cd starter-project
cp .env.example .env
# Edit .env with your keys
```

### 3. Start Services

```bash
# Start Qdrant + Backend
docker-compose up

# Or run just Qdrant locally if you prefer:
# docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 4. Test the API

```bash
# Check health
curl http://localhost:8000/health

# Store a memory
curl -X POST http://localhost:8000/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "Docker exit code 137 means OOM kill", "category": "tech"}'

# Search memories (semantic!)
curl -X POST http://localhost:8000/memories/search \
  -H "Content-Type: application/json" \
  -d '{"query": "why is my container dying", "limit": 3}'

# List all memories
curl http://localhost:8000/memories
```

## 🔌 Connect to Vapi (For Voice)

### Step 1: Expose Your Local Server

```bash
# Install ngrok
# Then expose port 8000
ngrok http 8000

# Copy the https URL (e.g., https://abc123.ngrok-free.app)
```

### Step 2: Update Environment

```bash
# In .env, set:
BACKEND_URL=https://abc123.ngrok-free.app
```

### Step 3: Configure Vapi Assistant

1. Go to https://vapi.ai/dashboard
2. Create a new Assistant
3. Get the assistant config:
   ```bash
   curl http://localhost:8000/vapi/assistant-config
   ```
4. Copy the JSON into your Vapi assistant settings
5. Set the Server URL to your ngrok URL + `/vapi/webhook`

### Step 4: Test Voice!

Click "Test Call" in Vapi dashboard and try:
- *"Remember that I have a meeting tomorrow at 3 PM"*
- *"What do I have scheduled tomorrow?"*

## 📁 Project Structure

```
starter-project/
├── docker-compose.yml      # Qdrant + FastAPI services
├── Dockerfile              # Backend container
├── requirements.txt        # Python deps
├── .env                    # Your secrets (gitignored)
├── .env.example            # Template
├── README.md               # This file
└── app/
    └── main.py             # FastAPI app with all endpoints
```

## 🔍 Key Concepts You'll Learn

### Qdrant (Vector Database)

```python
# Store with embedding
qdrant_client.upsert(
    collection_name="voice_memories",
    points=[PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,  # 1536-dimension vector
        payload={"content": "...", "category": "..."}
    )]
)

# Semantic search
results = qdrant_client.search(
    collection_name="voice_memories",
    query_vector=query_embedding,
    limit=3
)
```

### Vapi (Voice AI)

```python
# Webhook receives function calls from voice
@app.post("/vapi/webhook")
async def vapi_webhook(request: Request):
    # Vapi sends: {"message": {"type": "function-call", ...}}
    # You return: {"results": [{"result": "..."}]}
```

## 🧪 Experiments to Try

### 1. Test Semantic Search

Try these queries and observe how Qdrant finds relevant memories even with different words:

| Query | Should Find |
|-------|-------------|
| "why is my container dying" | "Docker exit code 137..." |
| "memory issue" | "OOM killer", "memory limits" |
| "when is my meeting" | "Meeting with Priya..." |

### 2. Play with Vapi Functions

Add more functions to `vapi/assistant-config`:

```json
{
  "name": "delete_memory",
  "description": "Delete a memory by content",
  "parameters": {...}
}
```

### 3. Try Different Embedding Models

Change in `main.py`:
```python
EMBEDDING_MODEL = "text-embedding-3-large"  # Better, more expensive
# or
EMBEDDING_MODEL = "text-embedding-ada-002"  # Older, cheaper
```

### 4. Add Memory Categories

Modify the schema to filter by category:
```python
results = qdrant_client.search(
    collection_name=COLLECTION_NAME,
    query_vector=embedding,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="tech"))]
    )
)
```

## 🎯 Idea Sparking Questions

As you play with this, ask yourself:

1. **What data would be valuable to search semantically?**
   - Logs, documentation, code, conversations, support tickets?

2. **What workflows could voice simplify?**
   - Creating tickets, querying dashboards, running commands?

3. **Who needs hands-free access to information?**
   - Developers, field workers, healthcare staff, drivers?

4. **What context should the AI remember across conversations?**
   - User preferences, past actions, project context?

## 📚 Resources

- **Qdrant Docs:** https://qdrant.tech/documentation/
- **Vapi Docs:** https://docs.vapi.ai/
- **Qdrant Discord:** (join from the problem statement)
- **Vapi Discord:** (join from the problem statement)

## 🐛 Troubleshooting

### Qdrant connection failed
```bash
# Check if Qdrant is running
docker ps
curl http://localhost:6333/dashboard/
```

### OpenAI errors
```bash
# Verify your API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Vapi webhook not reaching local
```bash
# Verify ngrok is working
curl https://your-ngrok-url.ngrok-free.app/health
```

---

**Happy experimenting!** Once you have a lightbulb moment, let's build your winning hackathon project. 🚀
