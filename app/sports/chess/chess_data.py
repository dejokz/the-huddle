"""
The Huddle - Chess Data Store
Simulated chess data for fantasy chess leagues and strategy advice
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class MatchMoment:
    moment_id: str
    match_id: str
    match_name: str
    round_num: str
    event_type: str
    description: str
    players_involved: List[str]
    context: str
    fantasy_impact: str
    venue: str
    timestamp: str = ""


@dataclass
class PlayerProfile:
    player_id: str
    name: str
    country: str
    title: str
    classical_rating: int
    rapid_rating: int
    blitz_rating: int
    recent_form: List[str] = field(default_factory=list)
    venue_stats: Dict[str, Dict] = field(default_factory=dict)
    vs_team_stats: Dict[str, Dict] = field(default_factory=dict)
    key_moments: List[str] = field(default_factory=list)
    fantasy_rating: str = "B"
    special_traits: List[str] = field(default_factory=list)


@dataclass
class StrategyInsight:
    strategy_id: str
    name: str
    category: str
    complexity: str
    win_rate_white: str
    win_rate_black: str
    draw_rate: str
    key_ideas: List[str] = field(default_factory=list)
    famous_practitioners: List[str] = field(default_factory=list)
    characteristics: List[str] = field(default_factory=list)


@dataclass
class FantasyScenario:
    scenario_id: str
    scenario_type: str
    match_id: str
    match_name: str
    options: List[str]
    recommendation: str
    reasoning: str
    alternative: Optional[str] = None
    alternative_reasoning: Optional[str] = None
    venue: str = ""
    match_situation: str = ""


# ==================== MATCH MOMENTS ====================

MATCH_MOMENTS = [
    MatchMoment(
        moment_id="chess_wc_2024_001",
        match_id="WCC2024_QF",
        match_name="FIDE World Cup 2024 Quarter-Final",
        round_num="Round 3",
        event_type="upset",
        description="Rameshbabu Praggnanandhaa stunned Magnus Carlsen in a rapid tiebreak. The 18-year-old Indian Grandmaster defended a difficult rook endgame and then outplayed Carlsen in the Armageddon decider. The chess world erupted in celebration.",
        players_involved=["Rameshbabu Praggnanandhaa", "Magnus Carlsen"],
        context="Pragg had already beaten Hikaru Nakamura earlier. Facing the World Champion was the ultimate test.",
        fantasy_impact="Praggnanandhaa was a massive differential pick. Owners who captained him got triple-digit fantasy returns.",
        venue="Baku, Azerbaijan",
        timestamp="2024-08-18"
    ),
    MatchMoment(
        moment_id="chess_candidates_2024_001",
        match_id="CANDIDATES2024_R14",
        match_name="FIDE Candidates 2024 Round 14",
        round_num="Round 14",
        event_type="title_clinch",
        description="Gukesh Dommaraju drew against Hikaru Nakamura to clinch the Candidates tournament. At just 17 years old, he became the youngest ever challenger for the World Chess Championship. The Indian teenager showed nerves of steel in the final round.",
        players_involved=["Gukesh Dommaraju", "Hikaru Nakamura"],
        context="Gukesh needed only a draw to win the tournament. The game was tense but he held his composure.",
        fantasy_impact="Gukesh owners celebrated huge fantasy gains. His consistency across 14 rounds made him an S-tier captain.",
        venue="Toronto, Canada",
        timestamp="2024-04-22"
    ),
    MatchMoment(
        moment_id="chess_tata_2025_001",
        match_id="TATA2025_M7",
        match_name="Tata Steel Chess 2025 Round 7",
        round_num="Round 7",
        event_type="brilliancy",
        description="Magnus Carlsen played a stunning queen sacrifice against Fabiano Caruana. The Norwegian sacrificed his queen for a devastating attack that forced checkmate in 8 moves. Commentators called it one of the greatest games in Tata Steel history.",
        players_involved=["Magnus Carlsen", "Fabiano Caruana"],
        context="Both players were tied for first place. Carlsen's brilliancy gave him a decisive lead.",
        fantasy_impact="Carlsen's win with a brilliancy bonus gave 15 fantasy points. A captaincy masterstroke.",
        venue="Wijk aan Zee, Netherlands",
        timestamp="2025-01-24"
    ),
    MatchMoment(
        moment_id="chess_sinquefield_2024_001",
        match_id="SINQ2024_R5",
        match_name="Sinquefield Cup 2024 Round 5",
        round_num="Round 5",
        event_type="comeback",
        description="Alireza Firouzja lost two games early in the tournament but mounted a stunning comeback with three consecutive wins. His victory over Wesley So in round 5 featured a brilliant tactical sequence in a complex Sicilian Najdorf.",
        players_involved=["Alireza Firouzja", "Wesley So"],
        context="Firouzja was in danger of finishing last. The comeback kept him in contention for the title.",
        fantasy_impact="Firouzja's comeback streak made him a differential hero. 13 points in round 5 alone.",
        venue="Saint Louis, USA",
        timestamp="2024-11-28"
    ),
    MatchMoment(
        moment_id="chess_norway_2024_001",
        match_id="NORWAY2024_R3",
        match_name="Norway Chess 2024 Round 3",
        round_num="Round 3",
        event_type="upset",
        description="Hikaru Nakamura defeated Magnus Carlsen in their classical encounter for the first time in over a decade. Nakamura played a flawless endgame, converting a slight material advantage with precision. The American celebrated with his signature enthusiasm.",
        players_involved=["Hikaru Nakamura", "Magnus Carlsen"],
        context="Carlsen was undefeated against Nakamura in classical chess for 10 years. The psychological barrier was broken.",
        fantasy_impact="Nakamura's historic win gave 12 points plus a massive psychological bonus in fantasy leagues.",
        venue="Stavanger, Norway",
        timestamp="2024-06-05"
    ),
    MatchMoment(
        moment_id="chess_olympiad_2024_001",
        match_id="OLYMPIAD2024_R9",
        match_name="Chess Olympiad 2024 Round 9",
        round_num="Round 9",
        event_type="clutch_win",
        description="Gukesh delivered a clutch win on board one against Fabiano Caruana to secure India's first-ever Olympiad gold medal. The game was balanced for 40 moves until Gukesh found a beautiful knight fork that decided the match.",
        players_involved=["Gukesh Dommaraju", "Fabiano Caruana"],
        context="India and USA were tied for gold. Gukesh's win on the top board sealed the historic victory.",
        fantasy_impact="Gukesh's clutch performance gave 14 fantasy points. The highest-pressure game of his career.",
        venue="Budapest, Hungary",
        timestamp="2024-09-22"
    ),
    MatchMoment(
        moment_id="chess_tata_2025_002",
        match_id="TATA2025_M10",
        match_name="Tata Steel Chess 2025 Round 10",
        round_num="Round 10",
        event_type="draw",
        description="Praggnanandhaa and Gukesh played a marathon 98-move draw. The all-Indian clash saw both players miss winning chances in a complex rook endgame. The draw kept both players in contention for the title.",
        players_involved=["Rameshbabu Praggnanandhaa", "Gukesh Dommaraju"],
        context="Both Indians were chasing Carlsen at the top. A draw was a fair result but neither gained ground.",
        fantasy_impact="The draw gave 2 points each. A safe but unspectacular return for fantasy owners.",
        venue="Wijk aan Zee, Netherlands",
        timestamp="2025-01-29"
    ),
    MatchMoment(
        moment_id="chess_speed_2024_001",
        match_id="SPEED2024_FINAL",
        match_name="Speed Chess Championship 2024 Final",
        round_num="Final",
        event_type="dominant_win",
        description="Magnus Carlsen crushed Hikaru Nakamura 19.5-10.5 in the Speed Chess Championship final. The Norwegian was simply unstoppable in bullet chess, winning game after game with ruthless efficiency. His online dominance continues.",
        players_involved=["Magnus Carlsen", "Hikaru Nakamura"],
        context="The two greatest speed chess players faced off. Carlsen proved why he is the undisputed king.",
        fantasy_impact="Carlsen's dominant performance gave maximum fantasy points. Essential pick for speed chess formats.",
        venue="Chess.com Online",
        timestamp="2024-12-15"
    ),
]


# ==================== PLAYER PROFILES ====================

PLAYER_PROFILES = [
    PlayerProfile(
        player_id="magnus_carlsen",
        name="Magnus Carlsen",
        country="Norway",
        title="Grandmaster",
        classical_rating=2830,
        rapid_rating=2839,
        blitz_rating=2886,
        recent_form=["Win", "Win", "Draw", "Win", "Win"],
        venue_stats={
            "Wijk aan Zee": {"wins": 8, "tournaments": 10, "avg": 8.5},
            "Baku": {"wins": 3, "tournaments": 2, "avg": 7.0}
        },
        vs_team_stats={
            "Nakamura": {"wins": 18, "losses": 4, "draws": 25},
            "Caruana": {"wins": 15, "losses": 5, "draws": 30}
        },
        key_moments=[
            "Queen sacrifice brilliancy vs Caruana at Tata Steel 2025",
            "Defeated by Praggnanandhaa at World Cup 2024",
            "Speed Chess Champion 2024"
        ],
        fantasy_rating="S",
        special_traits=["Endgame genius", "Universal style", "Mentally unbeatable"]
    ),
    PlayerProfile(
        player_id="hikaru_nakamura",
        name="Hikaru Nakamura",
        country="USA",
        title="Grandmaster",
        classical_rating=2788,
        rapid_rating=2804,
        blitz_rating=2879,
        recent_form=["Draw", "Loss", "Win", "Draw", "Win"],
        venue_stats={
            "Saint Louis": {"wins": 6, "tournaments": 8, "avg": 7.5},
            "Stavanger": {"wins": 2, "tournaments": 3, "avg": 6.0}
        },
        vs_team_stats={
            "Carlsen": {"wins": 4, "losses": 18, "draws": 25},
            "Caruana": {"wins": 8, "losses": 6, "draws": 15}
        },
        key_moments=[
            "First classical win over Carlsen in 10 years at Norway 2024",
            "Speed Chess runner-up 2024",
            "Streaming superstar with elite results"
        ],
        fantasy_rating="A",
        special_traits=["Speed chess king", "Tactical genius", "Streamer"]
    ),
    PlayerProfile(
        player_id="praggnanandhaa_r",
        name="Rameshbabu Praggnanandhaa",
        country="India",
        title="Grandmaster",
        classical_rating=2747,
        rapid_rating=2767,
        blitz_rating=2681,
        recent_form=["Win", "Draw", "Draw", "Win", "Draw"],
        venue_stats={
            "Baku": {"wins": 5, "tournaments": 1, "avg": 8.0},
            "Wijk aan Zee": {"wins": 3, "tournaments": 2, "avg": 6.5}
        },
        vs_team_stats={
            "Carlsen": {"wins": 2, "losses": 1, "draws": 3},
            "Gukesh": {"wins": 1, "losses": 1, "draws": 4}
        },
        key_moments=[
            "Upset Carlsen at World Cup 2024 tiebreaks",
            "Youngest to reach 2800 in rapid",
            "India's rising superstar"
        ],
        fantasy_rating="A",
        special_traits=["Calculator", "Endgame specialist", "Fearless"]
    ),
    PlayerProfile(
        player_id="gukesh_d",
        name="Gukesh Dommaraju",
        country="India",
        title="Grandmaster",
        classical_rating=2783,
        rapid_rating=2760,
        blitz_rating=2651,
        recent_form=["Win", "Draw", "Win", "Draw", "Win"],
        venue_stats={
            "Toronto": {"wins": 5, "tournaments": 1, "avg": 7.5},
            "Budapest": {"wins": 7, "tournaments": 1, "avg": 8.5}
        },
        vs_team_stats={
            "Caruana": {"wins": 3, "losses": 2, "draws": 3},
            "Nakamura": {"wins": 2, "losses": 2, "draws": 4}
        },
        key_moments=[
            "Youngest ever Candidates winner at 17",
            "Clutch win vs Caruana to win Olympiad gold for India",
            "World Championship challenger 2024"
        ],
        fantasy_rating="S",
        special_traits=["Ice-cold nerves", "Fighter", "Youngest challenger"]
    ),
    PlayerProfile(
        player_id="fabiano_caruana",
        name="Fabiano Caruana",
        country="USA",
        title="Grandmaster",
        classical_rating=2790,
        rapid_rating=2811,
        blitz_rating=2764,
        recent_form=["Loss", "Draw", "Win", "Draw", "Loss"],
        venue_stats={
            "Saint Louis": {"wins": 5, "tournaments": 6, "avg": 7.0},
            "Wijk aan Zee": {"wins": 4, "tournaments": 3, "avg": 6.5}
        },
        vs_team_stats={
            "Carlsen": {"wins": 5, "losses": 15, "draws": 30},
            "Gukesh": {"wins": 2, "losses": 3, "draws": 3}
        },
        key_moments=[
            "Victim of Carlsen's queen sacrifice at Tata Steel 2025",
            "Lost Olympiad decider to Gukesh",
            "Perennial world championship contender"
        ],
        fantasy_rating="A",
        special_traits=["Opening specialist", "Preparation monster", "Classical beast"]
    ),
    PlayerProfile(
        player_id="alireza_firouzja",
        name="Alireza Firouzja",
        country="France",
        title="Grandmaster",
        classical_rating=2757,
        rapid_rating=2772,
        blitz_rating=2904,
        recent_form=["Win", "Win", "Win", "Loss", "Loss"],
        venue_stats={
            "Saint Louis": {"wins": 4, "tournaments": 2, "avg": 6.5},
            "Wijk aan Zee": {"wins": 5, "tournaments": 2, "avg": 7.0}
        },
        vs_team_stats={
            "Carlsen": {"wins": 2, "losses": 3, "draws": 5},
            "Nakamura": {"wins": 3, "losses": 4, "draws": 4}
        },
        key_moments=[
            "Stunning comeback at Sinquefield Cup 2024",
            "Highest rated blitz player in history",
            "Young prodigy with explosive style"
        ],
        fantasy_rating="A",
        special_traits=["Blitz monster", "Comeback king", "Aggressive"]
    ),
]

# ==================== STRATEGY INSIGHTS ====================

STRATEGY_INSIGHTS = [
    StrategyInsight(
        strategy_id="sicilian_najdorf",
        name="Sicilian Najdorf",
        category="Opening",
        complexity="Very High",
        win_rate_white="32%",
        win_rate_black="38%",
        draw_rate="30%",
        key_ideas=[
            "Control the d4 square with the f6 knight",
            "Launch queenside counterplay with b5",
            "Prepare the e5 break in the center"
        ],
        famous_practitioners=["Magnus Carlsen", "Fabiano Caruana", "Bobby Fischer"],
        characteristics=[
            "Complex tactical battles",
            "Black fights for the initiative from move 1",
            "Requires deep theoretical knowledge",
            "Favorite of aggressive players"
        ]
    ),
    StrategyInsight(
        strategy_id="queens_gambit",
        name="Queen's Gambit Declined",
        category="Opening",
        complexity="Medium",
        win_rate_white="36%",
        win_rate_black="26%",
        draw_rate="38%",
        key_ideas=[
            "Solid central control",
            "Develop pieces harmoniously",
            "Trade pieces to relieve pressure"
        ],
        famous_practitioners=["Magnus Carlsen", "Anatoly Karpov", "Vladimir Kramnik"],
        characteristics=[
            "Extremely solid for Black",
            "Leads to rich positional middlegames",
            "Low risk of early disasters",
            "Preferred by classical specialists"
        ]
    ),
    StrategyInsight(
        strategy_id="kings_indian",
        name="King's Indian Defence",
        category="Opening",
        complexity="High",
        win_rate_white="35%",
        win_rate_black="37%",
        draw_rate="28%",
        key_ideas=[
            "Allow White to build a broad pawn center",
            "Attack the center from the flanks",
            "Kingside pawn storm with f5 and g5"
        ],
        famous_practitioners=["Garry Kasparov", "Hikaru Nakamura", "Bobby Fischer"],
        characteristics=[
            "Hypermodern approach",
            "Fiery kingside attacks",
            "High risk, high reward",
            "Creates imbalanced positions"
        ]
    ),
    StrategyInsight(
        strategy_id="endgame_technique",
        name="Rook Endgames",
        category="Endgame",
        complexity="High",
        win_rate_white="",
        win_rate_black="",
        draw_rate="55%",
        key_ideas=[
            "The Lucena and Philidor positions",
            "Active king and rook coordination",
            "Cutting off the enemy king"
        ],
        famous_practitioners=["Magnus Carlsen", "José Raúl Capablanca"],
        characteristics=[
            "Most common endgame in chess",
            "Small advantages often decisive",
            "Requires precision and patience",
            "Carlsen's signature strength"
        ]
    ),
]


# ==================== FANTASY SCENARIOS ====================

FANTASY_SCENARIOS = [
    FantasyScenario(
        scenario_id="chess_captaincy_001",
        scenario_type="captaincy",
        match_id="TATA2025",
        match_name="Tata Steel Chess 2025",
        options=["Magnus Carlsen", "Gukesh Dommaraju", "Fabiano Caruana"],
        recommendation="Magnus Carlsen",
        reasoning="Carlsen has won Tata Steel 8 times and is in devastating form after his queen sacrifice brilliancy. He dominates at Wijk aan Zee.",
        alternative="Gukesh Dommaraju",
        alternative_reasoning="If you want a differential, Gukesh is the in-form Indian superstar. But Carlsen's consistency is unmatched.",
        venue="Wijk aan Zee",
        match_situation="Classical tournament"
    ),
    FantasyScenario(
        scenario_id="chess_differential_001",
        scenario_type="differential",
        match_id="SPEED2024",
        match_name="Speed Chess Championship 2024",
        options=["Alireza Firouzja", "Praggnanandhaa R", "Hikaru Nakamura"],
        recommendation="Alireza Firouzja",
        reasoning="Low ownership but the highest blitz rating in history. In speed chess, his aggressive style creates huge fantasy upside.",
        alternative="Praggnanandhaa R",
        alternative_reasoning="Pragg is a rapid specialist and has beaten Carlsen before. A solid differential with lower risk.",
        venue="Chess.com Online",
        match_situation="Speed chess final"
    ),
    FantasyScenario(
        scenario_id="chess_classical_pick_001",
        scenario_type="classical_pick",
        match_id="CANDIDATES2024",
        match_name="FIDE Candidates 2024",
        options=["Gukesh Dommaraju", "Fabiano Caruana", "Hikaru Nakamura"],
        recommendation="Gukesh Dommaraju",
        reasoning="Gukesh won the Candidates with ice-cold consistency. In long classical events, his fighting spirit yields reliable fantasy returns.",
        alternative="Fabiano Caruana",
        alternative_reasoning="Caruana is the most prepared player in classical chess. If you prefer safety over ceiling, he's your pick.",
        venue="Toronto",
        match_situation="14-round classical marathon"
    ),
    FantasyScenario(
        scenario_id="chess_opening_strategy_001",
        scenario_type="opening_strategy",
        match_id="OPENING_MASTERY",
        match_name="Fantasy Opening Strategy",
        options=["Sicilian Najdorf", "Queen's Gambit Declined", "King's Indian Defence"],
        recommendation="Queen's Gambit Declined",
        reasoning="The QGD is rock solid and leads to fewer early disasters. In fantasy chess, avoiding losses is as important as scoring wins.",
        alternative="Sicilian Najdorf",
        alternative_reasoning="If your fantasy scoring heavily rewards wins, the Najdorf's high-risk style can deliver more decisive results.",
        venue="Any",
        match_situation="Opening repertoire advice"
    ),
    FantasyScenario(
        scenario_id="chess_matchup_001",
        scenario_type="matchup",
        match_id="WCC2025",
        match_name="World Championship 2025: Carlsen vs Gukesh",
        options=["Back Carlsen to dominate", "Gukesh upset on tiebreaks", "Draw-heavy match"],
        recommendation="Back Carlsen to dominate",
        reasoning="Carlsen's experience and endgame technique are unmatched. Over a 14-game match, his consistency usually prevails.",
        alternative="Gukesh upset on tiebreaks",
        alternative_reasoning="If the match goes to rapid tiebreaks, Gukesh's youth and energy could shock the world. A high-reward differential.",
        venue="Multiple cities",
        match_situation="World Championship final"
    ),
]


# Helper functions

def get_all_moments() -> List[MatchMoment]:
    return MATCH_MOMENTS


def get_all_players() -> List[PlayerProfile]:
    return PLAYER_PROFILES


def get_all_strategies() -> List[StrategyInsight]:
    return STRATEGY_INSIGHTS


def get_all_scenarios() -> List[FantasyScenario]:
    return FANTASY_SCENARIOS


def get_player_by_name(name: str) -> Optional[PlayerProfile]:
    for player in PLAYER_PROFILES:
        if player.name.lower() == name.lower():
            return player
    return None


def get_strategy_by_name(name: str) -> Optional[StrategyInsight]:
    for strategy in STRATEGY_INSIGHTS:
        if name.lower() in strategy.name.lower():
            return strategy
    return None
