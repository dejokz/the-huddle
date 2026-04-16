"""
The Huddle - Multi-Sport Fantasy Assist Platform
FastAPI backend for Vapi Squads
Returns raw data for Vapi's LLM to process
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

app = FastAPI(title="The Huddle - Multi-Sport Fantasy Assist")

# ------------------------------------------------------------------
# Sport handler registry
# ------------------------------------------------------------------
SPORT_HANDLERS = {}


def _load_handlers():
    """Lazy-load sport handlers so import errors don't crash startup."""
    global SPORT_HANDLERS
    if SPORT_HANDLERS:
        return

    try:
        from app.sports.cricket import (
            get_match_moment as cricket_match,
            get_player_stats as cricket_player,
            get_venue_insights as cricket_venue,
            get_fantasy_advice as cricket_fantasy,
            handle_general_query as cricket_general,
        )

        SPORT_HANDLERS["cricket"] = {
            "query_match_moment": cricket_match,
            "get_player_stats": cricket_player,
            "get_venue_insights": cricket_venue,
            "get_fantasy_advice": cricket_fantasy,
            "general_sport_query": cricket_general,
        }
        logger.info("[INIT] Cricket handler registered")
    except Exception as e:
        logger.error(f"[INIT] Cricket handler failed: {e}")

    try:
        from app.sports.football import (
            get_match_moment as football_match,
            get_player_stats as football_player,
            get_venue_insights as football_venue,
            get_fantasy_advice as football_fantasy,
            handle_general_query as football_general,
        )

        SPORT_HANDLERS["football"] = {
            "query_match_moment": football_match,
            "get_player_stats": football_player,
            "get_venue_insights": football_venue,
            "get_fantasy_advice": football_fantasy,
            "general_sport_query": football_general,
        }
        logger.info("[INIT] Football handler registered")
    except Exception as e:
        logger.error(f"[INIT] Football handler failed: {e}")

    try:
        from app.sports.chess import (
            get_match_moment as chess_match,
            get_player_stats as chess_player,
            get_venue_insights as chess_venue,
            get_fantasy_advice as chess_fantasy,
            handle_general_query as chess_general,
        )

        SPORT_HANDLERS["chess"] = {
            "query_match_moment": chess_match,
            "get_player_stats": chess_player,
            "get_venue_insights": chess_venue,
            "get_fantasy_advice": chess_fantasy,
            "general_sport_query": chess_general,
        }
        logger.info("[INIT] Chess handler registered")
    except Exception as e:
        logger.error(f"[INIT] Chess handler failed: {e}")


_load_handlers()


# ------------------------------------------------------------------
# Generic sport webhook dispatcher
# ------------------------------------------------------------------
async def dispatch_sport_webhook(sport: str, request: Request):
    """Handle Vapi tool-calls for a specific sport."""
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

            logger.info(f"[{sport.upper()}] {function_name}: {arguments}")

            handler_map = SPORT_HANDLERS.get(sport)
            if not handler_map:
                logger.error(f"[{sport.upper()}] No handler registered")
                return {"results": []}

            func = handler_map.get(function_name)
            if not func:
                logger.error(f"[{sport.upper()}] Unknown function: {function_name}")
                return {"results": []}

            # Call handler and extract response payload
            raw_result = func(**arguments)
            response_text = raw_result.get("response", json.dumps(raw_result, indent=2))

            logger.info(f"[{sport.upper()} RETURNING] {response_text[:150]}...")

            return {
                "results": [{
                    "toolCallId": tool_call_id,
                    "result": response_text
                }]
            }

        return {"results": []}

    except Exception as e:
        logger.error(f"[{sport.upper()} ERROR] {e}")
        traceback.print_exc()
        return {"results": []}


@app.post("/vapi/webhook/{sport}")
async def sport_webhook(sport: str, request: Request):
    """Dynamic webhook for any registered sport."""
    return await dispatch_sport_webhook(sport, request)


# Legacy redirect for backward compatibility
@app.post("/vapi/cricket-webhook")
async def legacy_cricket_webhook(request: Request):
    """Deprecated: use /vapi/webhook/cricket instead."""
    return await dispatch_sport_webhook("cricket", request)


@app.get("/")
async def root():
    return {
        "status": "running",
        "mode": "multi-sport-data-only",
        "sports": list(SPORT_HANDLERS.keys()),
    }
