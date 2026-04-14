"""
FINAL FIXED VERSION - Handles both function-call and tool-calls
"""

import os
import sys
import json
import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('final_debug.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="CricVoice - FINAL", version="3.0.0")

# Import cricket handler
try:
    from app.cricket_handler import (
        get_match_moment,
        get_player_stats,
        get_venue_insights,
        get_fantasy_advice,
        handle_general_query
    )
    CRICKET_AVAILABLE = True
    logger.info("[OK] Cricket handler loaded")
except ImportError as e:
    CRICKET_AVAILABLE = False
    logger.error(f"[ERROR] Cricket handler not available: {e}")

@app.post("/vapi/cricket-webhook")
async def cricket_webhook(request: Request):
    """
    Handle function calls from Vapi
    Supports both 'function-call' and 'tool-calls' message types
    """
    logger.info("=" * 80)
    logger.info("[WEBHOOK] Called")
    
    try:
        body = await request.json()
        message_type = body.get("message", {}).get("type")
        logger.info(f"[MESSAGE TYPE] {message_type}")
        
        # Handle function-call (older format)
        if message_type == "function-call":
            return await handle_function_call(body)
        
        # Handle tool-calls (newer format used by Vapi)
        elif message_type == "tool-calls":
            return await handle_tool_calls(body)
        
        # For all other message types, return empty
        else:
            logger.info(f"[IGNORED] {message_type}")
            return {"results": []}
        
    except Exception as e:
        logger.error(f"[WEBHOOK ERROR] {e}")
        logger.error(traceback.format_exc())
        return {"results": []}

async def handle_function_call(body):
    """Handle legacy function-call format"""
    function_call = body.get("message", {}).get("functionCall", {})
    function_name = function_call.get("name")
    parameters = function_call.get("parameters", {})
    tool_call_id = body.get("message", {}).get("toolCallId")
    
    logger.info(f"[FUNCTION-CALL] {function_name}: {parameters}")
    
    result = await execute_function(function_name, parameters)
    
    if result:
        return {
            "results": [{
                "toolCallId": tool_call_id,
                "result": result
            }]
        }
    return {"results": []}

async def handle_tool_calls(body):
    """Handle tool-calls format (new Vapi format)"""
    tool_calls = body.get("message", {}).get("toolCalls", [])
    logger.info(f"[TOOL-CALLS] Processing {len(tool_calls)} tool calls")
    
    results = []
    
    for tool_call in tool_calls:
        tool_call_id = tool_call.get("id")
        function_data = tool_call.get("function", {})
        function_name = function_data.get("name")
        
        # Parse arguments from JSON string or dict
        arguments = function_data.get("arguments", "{}")
        if isinstance(arguments, str):
            try:
                parameters = json.loads(arguments)
            except json.JSONDecodeError:
                logger.error(f"[ERROR] Failed to parse arguments: {arguments}")
                continue
        else:
            parameters = arguments
        
        logger.info(f"[TOOL-CALL] {function_name} (id: {tool_call_id}): {parameters}")
        
        result = await execute_function(function_name, parameters)
        
        if result:
            results.append({
                "toolCallId": tool_call_id,
                "result": result
            })
            logger.info(f"[RESULT] {result[:100]}...")
    
    logger.info(f"[RETURNING] {len(results)} results")
    return {"results": results}

async def execute_function(function_name, parameters):
    """Execute the cricket function and return result text"""
    if not CRICKET_AVAILABLE:
        return "Cricket handler not available"
    
    try:
        result = None
        
        if function_name == "query_match_moment":
            query = parameters.get("query", "")
            logger.info(f"[EXECUTING] get_match_moment({query})")
            result = get_match_moment(query)
            
        elif function_name == "get_player_stats":
            player_name = parameters.get("player_name", "")
            query = parameters.get("query", "")
            logger.info(f"[EXECUTING] get_player_stats({player_name}, {query})")
            result = get_player_stats(player_name, query)
            
        elif function_name == "get_venue_insights":
            venue_name = parameters.get("venue_name", "")
            logger.info(f"[EXECUTING] get_venue_insights({venue_name})")
            result = get_venue_insights(venue_name)
            
        elif function_name == "get_fantasy_advice":
            query = parameters.get("query", "")
            logger.info(f"[EXECUTING] get_fantasy_advice({query})")
            result = get_fantasy_advice(query)
            
        elif function_name == "general_cricket_query":
            query = parameters.get("query", "")
            logger.info(f"[EXECUTING] general_cricket_query({query})")
            result = handle_general_query(query)
        else:
            logger.warning(f"[UNKNOWN FUNCTION] {function_name}")
            return None
        
        if result and result.get("success"):
            response_text = result.get("response", "No information available")
            logger.info(f"[SUCCESS] {response_text[:100]}...")
            return response_text
        else:
            error = result.get("error", "Unknown error") if result else "No result"
            logger.error(f"[FAILED] {error}")
            return f"Sorry, I couldn't retrieve that information. {error}"
            
    except Exception as e:
        logger.error(f"[EXECUTION ERROR] {e}")
        logger.error(traceback.format_exc())
        return f"Error processing request: {str(e)}"

@app.get("/")
async def root():
    return {"status": "running", "service": "CricVoice FINAL", "cricket_available": CRICKET_AVAILABLE}

@app.get("/health")
async def health():
    return {"status": "healthy", "cricket_available": CRICKET_AVAILABLE}
