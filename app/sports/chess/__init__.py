"""
Chess sport module for The Huddle.
"""

from .chess_handler import (
    ChessQueryHandler,
    get_match_moment,
    get_player_stats,
    get_venue_insights,
    get_fantasy_advice,
    handle_general_query,
)
from .chess_data import get_player_by_name, get_strategy_by_name

__all__ = [
    "ChessQueryHandler",
    "get_match_moment",
    "get_player_stats",
    "get_venue_insights",
    "get_fantasy_advice",
    "handle_general_query",
    "get_player_by_name",
    "get_strategy_by_name",
]
