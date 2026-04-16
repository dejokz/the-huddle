"""
Football sport module for The Huddle.
"""

from .football_handler import (
    FootballQueryHandler,
    get_match_moment,
    get_player_stats,
    get_venue_insights,
    get_fantasy_advice,
    handle_general_query,
)
from .football_data import get_player_by_name, get_venue_by_name

__all__ = [
    "FootballQueryHandler",
    "get_match_moment",
    "get_player_stats",
    "get_venue_insights",
    "get_fantasy_advice",
    "handle_general_query",
    "get_player_by_name",
    "get_venue_by_name",
]
