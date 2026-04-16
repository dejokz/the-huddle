"""
The Huddle - Football Query Handler (Data-Only Pattern)
Returns structured JSON data for Vapi LLM to process
"""

import os
import json
from typing import Dict, List
from qdrant_client import QdrantClient
from app.sports.football.football_data import get_player_by_name, get_venue_by_name
from app.embeddings import LocalEmbedding

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")


class FootballQueryHandler:
    """Handle football-related queries - returns data only, no LLM processing"""
    sport = "football"

    def __init__(self):
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.embeddings = LocalEmbedding()

    def _get_embedding(self, text: str) -> List[float]:
        return self.embeddings.encode(text)

    def _format_data_response(self, data: Dict) -> str:
        return json.dumps(data, indent=2)

    def query_match_moments(self, query: str) -> Dict:
        try:
            embedding = self._get_embedding(query)
            results = self.qdrant.query_points(
                collection_name="football_match_moments",
                query=embedding,
                limit=3
            ).points

            moments = []
            for r in results:
                payload = r.payload
                moments.append({
                    "match": payload.get("match_name"),
                    "event": payload.get("event_type"),
                    "description": payload.get("description"),
                    "players": payload.get("players_involved", []),
                    "fantasy_impact": payload.get("fantasy_impact")
                })

            data = {
                "query": query,
                "type": "match_moments",
                "results_found": len(moments),
                "moments": moments
            }
            return {
                "success": True,
                "query": query,
                "response": self._format_data_response(data),
                "data": data
            }
        except Exception as e:
            print(f"[Error] query_match_moments: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": '{"error": "Could not retrieve match moments"}'
            }

    def query_player_stats(self, player_name: str, query: str = "") -> Dict:
        try:
            player = get_player_by_name(player_name)
            if player:
                player_data = {
                    "name": player.name,
                    "team": player.team,
                    "position": player.position,
                    "goals": player.goals_this_season,
                    "assists": player.assists_this_season,
                    "matches": player.matches_played,
                    "recent_form": player.recent_form,
                    "fantasy_rating": player.fantasy_rating,
                    "special_traits": player.special_traits,
                    "key_moments": player.key_moments
                }
                embedding = self._get_embedding(f"{player_name} performance stats")
                results = self.qdrant.query_points(
                    collection_name="football_players",
                    query=embedding,
                    limit=1
                ).points
                context = {"player_data": player_data}
                if results:
                    context["additional_context"] = results[0].payload
                return {
                    "success": True,
                    "player": player_name,
                    "response": self._format_data_response(context),
                    "data": context
                }
            else:
                embedding = self._get_embedding(query or f"{player_name} football stats")
                results = self.qdrant.query_points(
                    collection_name="football_players",
                    query=embedding,
                    limit=3
                ).points
                players = [r.payload for r in results]
                data = {
                    "query": query or f"stats for {player_name}",
                    "type": "player_search",
                    "players_found": len(players),
                    "players": players
                }
                return {
                    "success": True,
                    "player": player_name,
                    "response": self._format_data_response(data),
                    "data": data
                }
        except Exception as e:
            print(f"[Error] query_player_stats: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f'{{"error": "Could not find statistics for {player_name}"}}'
            }

    def query_venue_insights(self, venue_name: str) -> Dict:
        venue = get_venue_by_name(venue_name)
        try:
            if venue:
                venue_data = {
                    "name": venue.name,
                    "city": venue.city,
                    "pitch_type": venue.pitch_type,
                    "avg_home_goals": venue.avg_home_goals,
                    "avg_away_goals": venue.avg_away_goals,
                    "home_win_rate": venue.home_win_rate,
                    "capacity": venue.capacity,
                    "weather_factor": venue.weather_factor,
                    "characteristics": venue.characteristics
                }
                return {
                    "success": True,
                    "venue": venue_name,
                    "response": self._format_data_response(venue_data),
                    "data": venue_data
                }
            else:
                embedding = self._get_embedding(f"{venue_name} stadium pitch conditions")
                results = self.qdrant.query_points(
                    collection_name="football_venues",
                    query=embedding,
                    limit=2
                ).points
                venues = [r.payload for r in results]
                data = {
                    "venue_query": venue_name,
                    "type": "venue_search",
                    "venues_found": len(venues),
                    "venues": venues
                }
                return {
                    "success": True,
                    "venue": venue_name,
                    "response": self._format_data_response(data),
                    "data": data
                }
        except Exception as e:
            print(f"[Error] query_venue_insights: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f'{{"error": "Could not find information about {venue_name}"}}'
            }

    def query_fantasy_advice(self, query: str) -> Dict:
        try:
            embedding = self._get_embedding(query)
            results = self.qdrant.query_points(
                collection_name="football_fantasy_scenarios",
                query=embedding,
                limit=3
            ).points

            scenarios = []
            for r in results:
                payload = r.payload
                scenarios.append({
                    "type": payload.get("scenario_type"),
                    "match": payload.get("match_name"),
                    "options": payload.get("options", []),
                    "recommendation": payload.get("recommendation"),
                    "reasoning": payload.get("reasoning"),
                    "alternative": payload.get("alternative")
                })

            data = {
                "query": query,
                "type": "fantasy_advice",
                "scenarios_found": len(scenarios),
                "scenarios": scenarios
            }
            return {
                "success": True,
                "query": query,
                "response": self._format_data_response(data),
                "data": data
            }
        except Exception as e:
            print(f"[Error] query_fantasy_advice: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": '{"error": "Could not provide fantasy advice"}'
            }

    def handle_general_query(self, query: str) -> Dict:
        try:
            embedding = self._get_embedding(query)
            all_results = []
            for collection in ["football_match_moments", "football_players", "football_venues", "football_fantasy_scenarios"]:
                try:
                    results = self.qdrant.query_points(
                        collection_name=collection,
                        query=embedding,
                        limit=2
                    ).points
                    for r in results:
                        all_results.append({
                            "collection": collection,
                            "score": r.score,
                            "data": r.payload
                        })
                except Exception as e:
                    print(f"[Warning] Search failed for {collection}: {e}")

            all_results.sort(key=lambda x: x["score"], reverse=True)
            top_results = all_results[:3]
            data = {
                "query": query,
                "type": "general_search",
                "results_found": len(top_results),
                "results": top_results
            }
            return {
                "success": True,
                "query": query,
                "response": self._format_data_response(data),
                "data": data
            }
        except Exception as e:
            print(f"[Error] handle_general_query: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": '{"error": "Could not find information"}'
            }


# Singleton instance
football_handler = FootballQueryHandler()


def get_match_moment(query: str) -> Dict:
    return football_handler.query_match_moments(query)


def get_player_stats(player_name: str, query: str = "") -> Dict:
    return football_handler.query_player_stats(player_name, query)


def get_venue_insights(venue_name: str) -> Dict:
    return football_handler.query_venue_insights(venue_name)


def get_fantasy_advice(query: str) -> Dict:
    return football_handler.query_fantasy_advice(query)


def handle_general_query(query: str) -> Dict:
    return football_handler.handle_general_query(query)
