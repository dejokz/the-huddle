"""
Base handler interface for all sports.
Each sport implements these methods to return raw JSON data for Vapi.
"""

from abc import ABC, abstractmethod
from typing import Dict


class BaseSportHandler(ABC):
    """Abstract base class for sport-specific query handlers."""

    sport: str = ""

    @abstractmethod
    def query_match_moments(self, query: str) -> Dict:
        """Search for specific match moments / events."""
        pass

    @abstractmethod
    def query_player_stats(self, player_name: str, query: str = "") -> Dict:
        """Get player statistics and profiles."""
        pass

    @abstractmethod
    def query_venue_insights(self, venue_name: str) -> Dict:
        """Get venue / ground / strategy information."""
        pass

    @abstractmethod
    def query_fantasy_advice(self, query: str) -> Dict:
        """Get fantasy league recommendations."""
        pass

    @abstractmethod
    def handle_general_query(self, query: str) -> Dict:
        """Handle general sport queries across all collections."""
        pass
