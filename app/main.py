"""
Alternative: Return raw data instead of generated text
Let Vapi's LLM handle the natural language generation
"""

import os
import json
import logging
import traceback
from fastapi import FastAPI, Request
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI(title="CricVoice - Data Only Mode")

try:
    from app.cricket_handler import (
        get_match_moment,
        get_player_stats,
        get_venue_insights,
        get_fantasy_advice,
        handle_general_query
    )
    CRICKET_AVAILABLE = True
except ImportError as e:
    CRICKET_AVAILABLE = False
    logger.error(f"[ERROR] {e}")

@app.post("/vapi/cricket-webhook")
async def cricket_webhook(request: Request):
    """
    Returns RAW DATA instead of generated text.
    Vapi's GPT-5.4 will process this data and generate response.
    """
    try:
        body = await request.json()
        message_type = body.get("message", {}).get("type")
        
        if message_type in ["function-call", "tool-calls"]:
            # Extract function call details
            if message_type == "tool-calls":
                tool_calls = body.get("message", {}).get("toolCalls", [])
                if not tool_calls:
                    return {"results": []}
                tool_call = tool_calls[0]
                tool_call_id = tool_call.get("id")
                function_data = tool_call.get("function", {})
                function_name = function_data.get("name")
                arguments = function_data.get("arguments", "{}")
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
            else:
                function_call = body.get("message", {}).get("functionCall", {})
                function_name = function_call.get("name")
                arguments = function_call.get("parameters", {})
                tool_call_id = body.get("message", {}).get("toolCallId")
            
            logger.info(f"[CALL] {function_name}: {arguments}")
            
            if not CRICKET_AVAILABLE:
                return {"results": []}
            
            # Query database WITHOUT LLM processing
            raw_data = await get_raw_data(function_name, arguments)
            
            # Return RAW DATA as string for Vapi LLM to process
            # Vapi's GPT-5.4 will craft the natural language response
            data_string = format_data_for_vapi(raw_data)
            
            logger.info(f"[RETURNING DATA] {data_string[:150]}...")
            
            return {
                "results": [{
                    "toolCallId": tool_call_id,
                    "result": data_string
                }]
            }
        
        return {"results": []}
        
    except Exception as e:
        logger.error(f"[ERROR] {e}")
        return {"results": []}

async def get_raw_data(function_name, parameters):
    """Get data from Qdrant without LLM processing"""
    try:
        if function_name == "query_match_moment":
            query = parameters.get("query", "")
            # Query Qdrant directly, get top results
            from qdrant_client import QdrantClient
            from app.embeddings import LocalEmbedding
            
            client = QdrantClient("localhost:6333")
            embedding = LocalEmbedding().encode(query)
            
            results = client.query_points(
                collection_name="match_moments",
                query=embedding,
                limit=2
            ).points
            
            return {
                "query": query,
                "matches_found": len(results),
                "data": [r.payload for r in results]
            }
            
        elif function_name == "get_player_stats":
            player_name = parameters.get("player_name", "")
            from app.cricket_data import get_player_by_name
            return get_player_by_name(player_name)
            
        elif function_name == "get_venue_insights":
            venue_name = parameters.get("venue_name", "")
            from app.cricket_data import get_venue_by_name
            return get_venue_by_name(venue_name)
            
        elif function_name == "get_fantasy_advice":
            query = parameters.get("query", "")
            # Return fantasy scenarios
            from qdrant_client import QdrantClient
            from app.embeddings import LocalEmbedding
            
            client = QdrantClient("localhost:6333")
            embedding = LocalEmbedding().encode(query)
            
            results = client.query_points(
                collection_name="fantasy_scenarios",
                query=embedding,
                limit=2
            ).points
            
            return {
                "query": query,
                "scenarios": [r.payload for r in results]
            }
            
        else:
            return {"error": "Unknown function"}
            
    except Exception as e:
        logger.error(f"[DATA ERROR] {e}")
        return {"error": str(e)}

def format_data_for_vapi(raw_data):
    """
    Format raw data as a string that Vapi's LLM can process.
    The LLM will use this to generate a natural response.
    """
    if not raw_data:
        return "No data found for this query."
    
    if "error" in raw_data:
        return f"Error retrieving data: {raw_data['error']}"
    
    # Convert dict to formatted string
    # Vapi's GPT-5.4 will read this and craft a response
    return json.dumps(raw_data, indent=2)

@app.get("/")
async def root():
    return {"status": "running", "mode": "data-only", "cricket_available": CRICKET_AVAILABLE}
