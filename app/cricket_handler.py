"""
CricVoice - Cricket Query Handler (FREE Stack Version)
Uses:
- Local Embeddings (sentence-transformers/all-MiniLM-L6-v2) - FREE
- Groq LLM (Llama 3.1 70B) - FREE tier
"""

import os
import json
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from app.cricket_data import get_player_by_name, get_venue_by_name
from app.embeddings import LocalEmbedding, cosine_similarity

# Try to import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Groq not installed. LLM features will not work.")

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class CricketQueryHandler:
    """Handle cricket-related voice queries using FREE stack"""
    
    def __init__(self):
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.embeddings = LocalEmbedding()  # FREE, local
        
        # Initialize Groq if available
        if GROQ_AVAILABLE and GROQ_API_KEY:
            self.llm = Groq(api_key=GROQ_API_KEY)
            print("[CricketHandler] Groq LLM initialized")
        else:
            self.llm = None
            print("[CricketHandler] LLM not available - set GROQ_API_KEY")
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding using local model (FREE)"""
        return self.embeddings.encode(text)
    
    def _generate_response(self, query: str, context: List[Dict]) -> str:
        """Generate response using Groq LLM (FREE tier)"""
        if not self.llm:
            return "I'm sorry, the LLM is not configured. Please set GROQ_API_KEY."
        
        # Format context
        context_text = "\n\n".join([
            f"Context {i+1}:\n{json.dumps(item, indent=2)}"
            for i, item in enumerate(context[:3])
        ])
        
        system_prompt = """You are CricVoice, an expert cricket analyst specializing in IPL fantasy leagues.
You speak with the authority of a seasoned commentator.

Your style:
- Enthusiastic but knowledgeable
- Use cricket terminology naturally
- Give fantasy-relevant insights
- Be conversational, not robotic
- Keep responses concise (2-3 sentences max)
- Sound like you're recounting matches you watched live

Respond naturally as if speaking to a friend."""

        user_prompt = f"""User asked: "{query}"

Here is relevant information from the database:
{context_text}

Provide a natural, conversational response as CricVoice:"""

        try:
            response = self.llm.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",  # FREE tier - Llama 4 Scout (latest & fastest)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[Groq Error] {e}")
            # Fallback: return context summary
            return f"Based on the data: {context[0].get('description', 'No details available')}" if context else "I don't have that information."
    
    def query_match_moments(self, query: str) -> Dict:
        """Search for specific match moments"""
        try:
            embedding = self._get_embedding(query)
            
            results = self.qdrant.query_points(
                collection_name="match_moments",
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
                    "fantasy_impact": payload.get("fantasy_impact"),
                    "score": r.score
                })
            
            response_text = self._generate_response(query, moments)
            
            return {
                "success": True,
                "query": query,
                "response": response_text,
                "moments_found": len(moments),
                "moments": moments
            }
            
        except Exception as e:
            print(f"[Error] query_match_moments: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I couldn't find information about that match moment."
            }
    
    def query_player_stats(self, player_name: str, query: str = "") -> Dict:
        """Get player statistics and insights"""
        # First check direct lookup
        player = get_player_by_name(player_name)
        
        try:
            if player:
                # Direct match found
                player_data = {
                    "name": player.name,
                    "team": player.team,
                    "role": player.role,
                    "ipl_avg": player.ipl_career_avg,
                    "ipl_sr": player.ipl_strike_rate,
                    "recent_form": player.recent_form,
                    "fantasy_rating": player.fantasy_rating,
                    "special_traits": player.special_traits,
                    "key_moments": player.key_moments
                }
                
                # Also search for related context
                embedding = self._get_embedding(f"{player_name} performance stats")
                results = self.qdrant.query_points(
                    collection_name="player_context",
                    query=embedding,
                    limit=1
                ).points
                
                context = [player_data]
                if results:
                    context.append(results[0].payload)
                
                response_text = self._generate_response(
                    query or f"Tell me about {player_name}", 
                    context
                )
                
                return {
                    "success": True,
                    "player": player_name,
                    "response": response_text,
                    "stats": player_data
                }
            else:
                # Search in Qdrant
                embedding = self._get_embedding(query or f"{player_name} cricket stats")
                results = self.qdrant.query_points(
                    collection_name="player_context",
                    query=embedding,
                    limit=3
                ).points
                
                players = [r.payload for r in results]
                response_text = self._generate_response(
                    query or f"Tell me about {player_name}", 
                    players
                )
                
                return {
                    "success": True,
                    "player": player_name,
                    "response": response_text,
                    "players_found": len(players)
                }
                
        except Exception as e:
            print(f"[Error] query_player_stats: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f"I couldn't find statistics for {player_name}."
            }
    
    def query_venue_insights(self, venue_name: str) -> Dict:
        """Get venue/ground information"""
        venue = get_venue_by_name(venue_name)
        
        try:
            if venue:
                venue_data = {
                    "name": venue.name,
                    "city": venue.city,
                    "pitch_type": venue.pitch_type,
                    "avg_first_innings": venue.avg_first_innings,
                    "avg_second_innings": venue.avg_second_innings,
                    "chase_success_rate": venue.chase_success_rate,
                    "boundary_size": venue.boundary_size,
                    "dew_factor": venue.dew_factor,
                    "characteristics": venue.characteristics
                }
                
                response_text = self._generate_response(
                    f"How is the pitch at {venue_name}?",
                    [venue_data]
                )
                
                return {
                    "success": True,
                    "venue": venue_name,
                    "response": response_text,
                    "details": venue_data
                }
            else:
                # Search in Qdrant
                embedding = self._get_embedding(f"{venue_name} stadium pitch conditions")
                results = self.qdrant.query_points(
                    collection_name="venue_insights",
                    query=embedding,
                    limit=2
                ).points
                
                venues = [r.payload for r in results]
                response_text = self._generate_response(f"Tell me about {venue_name}", venues)
                
                return {
                    "success": True,
                    "venue": venue_name,
                    "response": response_text
                }
                
        except Exception as e:
            print(f"[Error] query_venue_insights: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": f"I couldn't find information about {venue_name}."
            }
    
    def query_fantasy_advice(self, query: str) -> Dict:
        """Get fantasy league recommendations"""
        try:
            embedding = self._get_embedding(query)
            
            results = self.qdrant.query_points(
                collection_name="fantasy_scenarios",
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
            
            response_text = self._generate_response(query, scenarios)
            
            return {
                "success": True,
                "query": query,
                "response": response_text,
                "recommendations": len(scenarios)
            }
            
        except Exception as e:
            print(f"[Error] query_fantasy_advice: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I couldn't provide fantasy advice right now."
            }
    
    def handle_general_query(self, query: str) -> Dict:
        """Handle general cricket queries by searching all collections"""
        try:
            embedding = self._get_embedding(query)
            
            # Search across all collections
            all_results = []
            
            for collection in ["match_moments", "player_context", "venue_insights", "fantasy_scenarios"]:
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
                            "payload": r.payload
                        })
                except Exception as e:
                    print(f"[Warning] Search failed for {collection}: {e}")
            
            # Sort by relevance
            all_results.sort(key=lambda x: x["score"], reverse=True)
            
            # Take top 3
            top_results = all_results[:3]
            context = [r["payload"] for r in top_results]
            
            response_text = self._generate_response(query, context)
            
            return {
                "success": True,
                "query": query,
                "response": response_text,
                "sources": [r["collection"] for r in top_results]
            }
            
        except Exception as e:
            print(f"[Error] handle_general_query: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I'm having trouble finding that information."
            }


# Create singleton instance
cricket_handler = CricketQueryHandler()

# Convenience functions for webhook
def get_match_moment(query: str) -> Dict:
    return cricket_handler.query_match_moments(query)

def get_player_stats(player_name: str, query: str = "") -> Dict:
    return cricket_handler.query_player_stats(player_name, query)

def get_venue_insights(venue_name: str) -> Dict:
    return cricket_handler.query_venue_insights(venue_name)

def get_fantasy_advice(query: str) -> Dict:
    return cricket_handler.query_fantasy_advice(query)

def handle_general_query(query: str) -> Dict:
    return cricket_handler.handle_general_query(query)
