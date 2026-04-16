"""
The Huddle - Football Data Store
Simulated match data from Premier League & Champions League
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class MatchMoment:
    moment_id: str
    match_id: str
    match_name: str
    minute: str
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
    team: str
    position: str
    goals_this_season: int
    assists_this_season: int
    matches_played: int
    recent_form: List[int] = field(default_factory=list)
    venue_stats: Dict[str, Dict] = field(default_factory=dict)
    vs_team_stats: Dict[str, Dict] = field(default_factory=dict)
    key_moments: List[str] = field(default_factory=list)
    fantasy_rating: str = "B"
    special_traits: List[str] = field(default_factory=list)


@dataclass
class VenueInsight:
    venue_id: str
    name: str
    city: str
    pitch_type: str
    avg_home_goals: float
    avg_away_goals: float
    home_win_rate: str
    capacity: str
    weather_factor: str
    highest_score: str
    lowest_score: str
    batting_favorites: Dict[str, str] = field(default_factory=dict)
    bowling_favorites: Dict[str, str] = field(default_factory=dict)
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
        moment_id="epl_mci_ars_001",
        match_id="EPL2026_M12_MCIvARS",
        match_name="Man City vs Arsenal, Premier League 2026",
        minute="34",
        event_type="goal",
        description="Erling Haaland scored a thunderous volley from 25 yards out. The ball rocketed into the top corner leaving the Arsenal keeper with no chance. It was his 12th goal of the season and a statement finish.",
        players_involved=["Erling Haaland", "Martin Odegaard"],
        context="City were dominating possession but Arsenal were defending deep. Haaland's goal broke the deadlock.",
        fantasy_impact="Haaland owners got 10 points for the goal plus 3 bonus points. Must-have captain material.",
        venue="Etihad Stadium, Manchester",
        timestamp="2026-01-15"
    ),
    MatchMoment(
        moment_id="epl_liv_mun_001",
        match_id="EPL2026_M8_LIVvMUN",
        match_name="Liverpool vs Man United, Premier League 2026",
        minute="67",
        event_type="penalty_miss",
        description="Mohamed Salah stepped up to take a crucial penalty with Liverpool leading 1-0. His shot was well-saved by Andre Onana who dived to his left. The Anfield crowd groaned as Salah held his head in his hands.",
        players_involved=["Mohamed Salah", "Andre Onana"],
        context="Liverpool were pushing for a second goal to kill the game. The miss gave United hope.",
        fantasy_impact="Salah lost 2 points for the missed penalty. Onana gained 5 save points and a clean sheet bonus.",
        venue="Anfield, Liverpool",
        timestamp="2026-01-08"
    ),
    MatchMoment(
        moment_id="ucl_real_bvb_001",
        match_id="UCL2026_SF_RMAvBVB",
        match_name="Real Madrid vs Borussia Dortmund, UCL Semi-Final",
        minute="89",
        event_type="late_winner",
        description="Jude Bellingham scored a dramatic last-minute winner against his former club. He received the ball on the edge of the box, beat two defenders with a silky dribble, and curled the ball into the far corner.",
        players_involved=["Jude Bellingham", "Vinicius Jr"],
        context="1-1 in the dying minutes of the semi-final first leg. Bellingham's goal gave Madrid a crucial advantage.",
        fantasy_impact="Bellingham delivered 13 points including goal, assist, and bonus. A differential captain gem.",
        venue="Santiago Bernabeu, Madrid",
        timestamp="2026-04-22"
    ),
    MatchMoment(
        moment_id="epl_ars_che_001",
        match_id="EPL2026_M5_ARSvCHE",
        match_name="Arsenal vs Chelsea, Premier League 2026",
        minute="23",
        event_type="hat_trick",
        description="Bukayo Saka produced a masterclass against Chelsea, scoring a brilliant hat-trick. His first was a composed finish, the second a curling effort from outside the box, and the third a calm penalty.",
        players_involved=["Bukayo Saka", "Declan Rice"],
        context="Arsenal were looking to close the gap on league leaders. Saka's hat-trick essentially won the match by half-time.",
        fantasy_impact="Saka owners were rewarded with 20 points. Triple captain territory for sure.",
        venue="Emirates Stadium, London",
        timestamp="2026-02-01"
    ),
    MatchMoment(
        moment_id="epl_mun_liv_001",
        match_id="EPL2026_M18_MUNvLIV",
        match_name="Man United vs Liverpool, Premier League 2026",
        minute="45+2",
        event_type="red_card",
        description="Bruno Fernandes received a straight red card for a reckless studs-up challenge on Alexis Mac Allister. United were already trailing 2-0 and the red card effectively ended any chance of a comeback.",
        players_involved=["Bruno Fernandes", "Alexis Mac Allister"],
        context="United under pressure at home. The red card meant they played the entire second half with 10 men.",
        fantasy_impact="Bruno lost 3 points for the red card. A disaster for the 35% of managers who captained him.",
        venue="Old Trafford, Manchester",
        timestamp="2026-03-05"
    ),
    MatchMoment(
        moment_id="epl_mci_new_001",
        match_id="EPL2026_M22_MCIvNEW",
        match_name="Man City vs Newcastle, Premier League 2026",
        minute="56",
        event_type="assist",
        description="Kevin De Bruyne delivered a pin-point 40-yard pass to Phil Foden who controlled it brilliantly and finished past the keeper. The assist showcased De Bruyne's world-class vision.",
        players_involved=["Kevin De Bruyne", "Phil Foden"],
        context="City were searching for a breakthrough against a stubborn Newcastle defense.",
        fantasy_impact="De Bruyne got 6 points for the assist and 3 bonus points. Essential midfield pick.",
        venue="Etihad Stadium, Manchester",
        timestamp="2026-03-18"
    ),
    MatchMoment(
        moment_id="epl_ars_tot_001",
        match_id="EPL2026_M14_ARSvTOT",
        match_name="Arsenal vs Tottenham, North London Derby",
        minute="12",
        event_type="free_kick_goal",
        description="Martin Odegaard scored a stunning free-kick that bent over the wall and dipped into the top corner. The Tottenham goalkeeper was rooted to the spot as the ball nestled in the net.",
        players_involved=["Martin Odegaard", "Son Heung-min"],
        context="Early North London derby tension. Odegaard's goal set the tone for a dominant Arsenal performance.",
        fantasy_impact="Odegaard returned 9 points. A solid differential captain for the derby.",
        venue="Emirates Stadium, London",
        timestamp="2026-02-15"
    ),
    MatchMoment(
        moment_id="epl_liv_bha_001",
        match_id="EPL2026_M10_LIVvBHA",
        match_name="Liverpool vs Brighton, Premier League 2026",
        minute="78",
        event_type="goal",
        description="Marcus Rashford came off the bench for Liverpool and scored within 5 minutes. A blistering run down the left wing ended with a powerful near-post finish. The Liverpool fans chanted his name.",
        players_involved=["Marcus Rashford", "Trent Alexander-Arnold"],
        context="Liverpool needed a winner against a resilient Brighton side.",
        fantasy_impact="Rashford's super-sub appearance gave 8 points from limited minutes. Great bench boost.",
        venue="Anfield, Liverpool",
        timestamp="2026-01-25"
    ),
    MatchMoment(
        moment_id="ucl_bay_mci_001",
        match_id="UCL2026_QF_BAYvMCI",
        match_name="Bayern Munich vs Man City, UCL Quarter-Final",
        minute="41",
        event_type="goal",
        description="Erling Haaland scored a clinical header from a corner. He rose highest above two Bayern defenders and directed the ball into the bottom corner. Bayern's keeper had no chance.",
        players_involved=["Erling Haaland", "Bernardo Silva"],
        context="City leading 1-0 away in Munich. Haaland's header doubled the advantage before half-time.",
        fantasy_impact="Haaland with another haul - 10 points and 3 bonus. Essential for UCL fantasy.",
        venue="Allianz Arena, Munich",
        timestamp="2026-04-08"
    ),
    MatchMoment(
        moment_id="epl_che_mun_001",
        match_id="EPL2026_M16_CHEvMUN",
        match_name="Chelsea vs Man United, Premier League 2026",
        minute="55",
        event_type="own_goal",
        description="A calamitous own goal by Chelsea's defender who tried to clear a Marcus Rashford cross but sliced it into his own net. The Chelsea goalkeeper could only watch in despair.",
        players_involved=["Marcus Rashford"],
        context="United were applying pressure and the own goal gifted them the lead.",
        fantasy_impact="Rashford was credited with the assist for the own goal. 4 points total.",
        venue="Stamford Bridge, London",
        timestamp="2026-02-28"
    ),
    MatchMoment(
        moment_id="epl_mci_liv_001",
        match_id="EPL2026_M20_MCIvLIV",
        match_name="Man City vs Liverpool, Premier League 2026",
        minute="88",
        event_type="clean_sheet",
        description="Ederson made a spectacular diving save to deny Darwin Nunez a late equaliser. The save preserved City's clean sheet and earned them all three points in a tight title race encounter.",
        players_involved=["Ederson", "Darwin Nunez"],
        context="City leading 2-1. Nunez had a clear one-on-one chance.",
        fantasy_impact="Ederson owners celebrated 4 clean sheet points plus a save point. Goalkeepers can win you FPL.",
        venue="Etihad Stadium, Manchester",
        timestamp="2026-03-22"
    ),
    MatchMoment(
        moment_id="epl_tot_ars_001",
        match_id="EPL2026_M24_TOTvARS",
        match_name="Tottenham vs Arsenal, North London Derby",
        minute="64",
        event_type="goal",
        description="Declan Rice scored a screamer from 30 yards out. The ball took a slight deflection and looped over the Tottenham goalkeeper. Rice celebrated passionately in front of the away fans.",
        players_involved=["Declan Rice", "Bukayo Saka"],
        context="Arsenal leading 1-0. Rice's incredible strike sealed the derby victory.",
        fantasy_impact="Rice's goal plus clean sheet bonus gave 11 points. A must-own defensive midfielder.",
        venue="Tottenham Hotspur Stadium, London",
        timestamp="2026-04-05"
    ),
]


# ==================== PLAYER PROFILES ====================

PLAYER_PROFILES = [
    PlayerProfile(
        player_id="erling_haaland",
        name="Erling Haaland",
        team="Man City",
        position="Forward",
        goals_this_season=28,
        assists_this_season=5,
        matches_played=32,
        recent_form=[2, 1, 1, 0, 1],
        venue_stats={
            "Etihad Stadium": {"goals": 18, "matches": 16, "avg": 1.1},
            "Anfield": {"goals": 2, "matches": 3, "avg": 0.7}
        },
        vs_team_stats={
            "Arsenal": {"goals": 4, "matches": 4},
            "Liverpool": {"goals": 3, "matches": 4}
        },
        key_moments=[
            "28 goals in Premier League 2026",
            "Thunderous volley vs Arsenal",
            "Clinical header vs Bayern Munich"
        ],
        fantasy_rating="S",
        special_traits=["Goal machine", "Penalty box predator", "Captain must-have"]
    ),
    PlayerProfile(
        player_id="mohamed_salah",
        name="Mohamed Salah",
        team="Liverpool",
        position="Forward",
        goals_this_season=22,
        assists_this_season=12,
        matches_played=33,
        recent_form=[0, 1, 1, 1, 0],
        venue_stats={
            "Anfield": {"goals": 15, "matches": 16, "avg": 0.9}
        },
        vs_team_stats={
            "Man United": {"goals": 8, "matches": 6},
            "Man City": {"goals": 5, "matches": 5}
        },
        key_moments=[
            "Penalty miss vs Man United",
            "22 goals and 12 assists in 2026",
            "Liverpool's talisman"
        ],
        fantasy_rating="S",
        special_traits=["Penalty taker", "Consistent", "Assist provider"]
    ),
    PlayerProfile(
        player_id="jude_bellingham",
        name="Jude Bellingham",
        team="Real Madrid",
        position="Midfielder",
        goals_this_season=18,
        assists_this_season=10,
        matches_played=30,
        recent_form=[1, 1, 0, 1, 1],
        venue_stats={
            "Santiago Bernabeu": {"goals": 12, "matches": 15, "avg": 0.8}
        },
        vs_team_stats={
            "Barcelona": {"goals": 3, "matches": 3},
            "Dortmund": {"goals": 2, "matches": 2}
        },
        key_moments=[
            "Late winner vs Dortmund in UCL semi-final",
            "18 goals from midfield in 2026",
            "England's golden boy"
        ],
        fantasy_rating="A",
        special_traits=["Box-to-box", "Big game player", "Differential captain"]
    ),
    PlayerProfile(
        player_id="bukayo_saka",
        name="Bukayo Saka",
        team="Arsenal",
        position="Forward",
        goals_this_season=19,
        assists_this_season=14,
        matches_played=34,
        recent_form=[3, 0, 1, 1, 0],
        venue_stats={
            "Emirates Stadium": {"goals": 14, "matches": 17, "avg": 0.8}
        },
        vs_team_stats={
            "Chelsea": {"goals": 6, "matches": 4},
            "Tottenham": {"goals": 5, "matches": 5}
        },
        key_moments=[
            "Hat-trick vs Chelsea",
            "Arsenal's star boy",
            "Penalty and set-piece taker"
        ],
        fantasy_rating="A",
        special_traits=["Dribbler", "Set-piece threat", "Young talent"]
    ),
    PlayerProfile(
        player_id="bruno_fernandes",
        name="Bruno Fernandes",
        team="Man United",
        position="Midfielder",
        goals_this_season=10,
        assists_this_season=11,
        matches_played=31,
        recent_form=[0, 0, 1, 0, 0],
        venue_stats={
            "Old Trafford": {"goals": 7, "matches": 15, "avg": 0.5}
        },
        vs_team_stats={
            "Liverpool": {"goals": 2, "matches": 4},
            "Chelsea": {"goals": 3, "matches": 4}
        },
        key_moments=[
            "Red card vs Liverpool",
            "Penalty taker for United",
            "High-risk, high-reward pick"
        ],
        fantasy_rating="B",
        special_traits=["Penalty taker", "Creative", "Hot-headed"]
    ),
    PlayerProfile(
        player_id="martin_odegaard",
        name="Martin Odegaard",
        team="Arsenal",
        position="Midfielder",
        goals_this_season=12,
        assists_this_season=15,
        matches_played=33,
        recent_form=[1, 0, 1, 1, 0],
        venue_stats={
            "Emirates Stadium": {"goals": 9, "matches": 16, "avg": 0.6}
        },
        vs_team_stats={
            "Tottenham": {"goals": 4, "matches": 4},
            "Chelsea": {"goals": 2, "matches": 4}
        },
        key_moments=[
            "Stunning free-kick vs Tottenham",
            "Arsenal captain and playmaker",
            "Set-piece specialist"
        ],
        fantasy_rating="A",
        special_traits=["Playmaker", "Set-piece specialist", "Captain"]
    ),
    PlayerProfile(
        player_id="marcus_rashford",
        name="Marcus Rashford",
        team="Liverpool",
        position="Forward",
        goals_this_season=14,
        assists_this_season=8,
        matches_played=29,
        recent_form=[1, 0, 0, 1, 1],
        venue_stats={
            "Anfield": {"goals": 10, "matches": 14, "avg": 0.7}
        },
        vs_team_stats={
            "Chelsea": {"goals": 5, "matches": 4},
            "Man City": {"goals": 3, "matches": 4}
        },
        key_moments=[
            "Super-sub winner vs Brighton",
            "Moved to Liverpool in 2025",
            "Pace and finishing threat"
        ],
        fantasy_rating="A",
        special_traits=["Pace", "Super sub", "Differential"]
    ),
    PlayerProfile(
        player_id="kevin_de_bruyne",
        name="Kevin De Bruyne",
        team="Man City",
        position="Midfielder",
        goals_this_season=6,
        assists_this_season=21,
        matches_played=28,
        recent_form=[0, 2, 1, 0, 1],
        venue_stats={
            "Etihad Stadium": {"assists": 14, "matches": 14, "avg": 1.0}
        },
        vs_team_stats={
            "Arsenal": {"assists": 4, "matches": 4},
            "Liverpool": {"assists": 3, "matches": 4}
        },
        key_moments=[
            "40-yard assist to Foden vs Newcastle",
            "21 assists in Premier League 2026",
            "World-class vision and passing"
        ],
        fantasy_rating="S",
        special_traits=["Assist king", "Vision", "Set-piece taker"]
    ),
]


# ==================== VENUE INSIGHTS ====================

VENUE_INSIGHTS = [
    VenueInsight(
        venue_id="old_trafford",
        name="Old Trafford",
        city="Manchester",
        pitch_type="Balanced with good grass",
        avg_home_goals=1.8,
        avg_away_goals=1.2,
        home_win_rate="58%",
        capacity="74,310",
        weather_factor="Rainy winters can slow the pitch",
        highest_score="8-2 vs Arsenal (2011)",
        lowest_score="0-5 vs Liverpool (2021)",
        characteristics=[
            "Large pitch favors wingers",
            "Atmospheric pressure on visitors",
            "Good drainage despite rain",
            "Historic theater of dreams"
        ]
    ),
    VenueInsight(
        venue_id="anfield",
        name="Anfield",
        city="Liverpool",
        pitch_type="Fast and smooth",
        avg_home_goals=2.2,
        avg_away_goals=0.9,
        home_win_rate="72%",
        capacity="61,276",
        weather_factor="Wind from River Mersey affects long balls",
        highest_score="9-0 vs Bournemouth (2022)",
        lowest_score="0-4 vs Man City (2021)",
        characteristics=[
            "Intimidating atmosphere",
            "Kop end drives team forward",
            "Fast surface suits pressing",
            "Strong home advantage"
        ]
    ),
]


# ==================== FANTASY SCENARIOS ====================

FANTASY_SCENARIOS = [
    FantasyScenario(
        scenario_id="captaincy_epl_001",
        scenario_type="captaincy",
        match_id="EPL2026_M12_MCIvARS",
        match_name="Man City vs Arsenal",
        options=["Erling Haaland", "Bukayo Saka", "Kevin De Bruyne"],
        recommendation="Erling Haaland",
        reasoning="Haaland has 28 goals this season and loves playing at the Etihad. Against Arsenal's high line, his pace and finishing will be lethal.",
        alternative="Bukayo Saka",
        alternative_reasoning="Saka is in hot form with a recent hat-trick, but Haaland's ceiling is higher.",
        venue="Etihad Stadium",
        match_situation="Title race clash"
    ),
    FantasyScenario(
        scenario_id="differential_epl_001",
        scenario_type="differential",
        match_id="EPL2026_M8_LIVvMUN",
        match_name="Liverpool vs Man United",
        options=["Martin Odegaard", "Marcus Rashford", "Declan Rice"],
        recommendation="Martin Odegaard",
        reasoning="Low ownership but high upside. Arsenal's captain takes set-pieces and has been delivering consistent returns.",
        alternative="Marcus Rashford",
        alternative_reasoning="If playing as a super-sub, Rashford could deliver explosive minutes-per-point value.",
        venue="Anfield",
        match_situation="Red derby"
    ),
    FantasyScenario(
        scenario_id="midfield_pick_001",
        scenario_type="midfield_pick",
        match_id="EPL2026_M22_MCIvNEW",
        match_name="Man City vs Newcastle",
        options=["Kevin De Bruyne", "Jude Bellingham", "Bruno Fernandes"],
        recommendation="Kevin De Bruyne",
        reasoning="21 assists this season. Against Newcastle's compact defense, his vision and through-balls will unlock chances.",
        alternative="Jude Bellingham",
        alternative_reasoning="If you need a differential, Bellingham combines goals and assists in big games.",
        venue="Etihad Stadium",
        match_situation="Champions chasing 3 points"
    ),
    FantasyScenario(
        scenario_id="defensive_stack_001",
        scenario_type="defensive_stack",
        match_id="EPL2026_M20_MCIvLIV",
        match_name="Man City vs Liverpool",
        options=["Man City defense", "Liverpool defense", "Both teams to score"],
        recommendation="Man City defense",
        reasoning="City have the best defensive record at home. Ederson is reliable and the back four rarely concedes at the Etihad.",
        alternative="Both teams to score",
        alternative_reasoning="If you expect an open game, skip clean sheets and load up on attackers from both sides.",
        venue="Etihad Stadium",
        match_situation="Top-of-the-table clash"
    ),
    FantasyScenario(
        scenario_id="fixture_difficulty_001",
        scenario_type="fixture_difficulty",
        match_id="EPL2026_GW25",
        match_name="Gameweek 25 Fixtures",
        options=["Triple up on City attackers", "Back Arsenal vs weak opposition", "Bench Salah vs tough defense"],
        recommendation="Back Arsenal vs weak opposition",
        reasoning="Arsenal have a kind run of fixtures. Saka and Odegaard should feast on lower-table teams.",
        alternative="Triple up on City attackers",
        alternative_reasoning="If you have the funds, Haaland + Foden + De Bruyne is a template-breaking strategy.",
        venue="Multiple",
        match_situation="Gameweek 25 planning"
    ),
    FantasyScenario(
        scenario_id="ucl_captaincy_001",
        scenario_type="captaincy",
        match_id="UCL2026_SF_RMAvBVB",
        match_name="Real Madrid vs Dortmund",
        options=["Jude Bellingham", "Vinicius Jr", "Erling Haaland"],
        recommendation="Jude Bellingham",
        reasoning="Playing against his former club at the Bernabeu. He thrives in UCL knockouts and already scored the late winner in the first leg.",
        alternative="Vinicius Jr",
        alternative_reasoning="If Madrid get early counters, Vinicius's pace could destroy Dortmund on the break.",
        venue="Santiago Bernabeu",
        match_situation="UCL Semi-Final second leg"
    ),
]


# Helper functions

def get_all_moments() -> List[MatchMoment]:
    return MATCH_MOMENTS


def get_all_players() -> List[PlayerProfile]:
    return PLAYER_PROFILES


def get_all_venues() -> List[VenueInsight]:
    return VENUE_INSIGHTS


def get_all_scenarios() -> List[FantasyScenario]:
    return FANTASY_SCENARIOS


def get_player_by_name(name: str) -> Optional[PlayerProfile]:
    for player in PLAYER_PROFILES:
        if player.name.lower() == name.lower():
            return player
    return None


def get_venue_by_name(name: str) -> Optional[VenueInsight]:
    for venue in VENUE_INSIGHTS:
        if name.lower() in venue.name.lower():
            return venue
    return None
