"""
CricVoice - Cricket Data Store
Simulated match data from IPL 2026 (extracted from Cricbuzz)
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MatchMoment:
    """A key moment from a match with fantasy context"""
    moment_id: str
    match_id: str
    match_name: str
    over: str
    event_type: str  # wicket, six, four, milestone, etc.
    description: str  # Rich commentary-style description
    players_involved: List[str]
    context: str  # Match situation at that point
    fantasy_impact: str
    venue: str
    timestamp: str = ""

@dataclass
class PlayerProfile:
    """Player statistics and context"""
    player_id: str
    name: str
    team: str
    role: str  # batsman, bowler, all-rounder, wicketkeeper
    
    # Overall stats
    ipl_career_avg: float
    ipl_strike_rate: float
    matches_played: int
    
    # Recent form (last 5 innings/scores)
    recent_form: List[int] = field(default_factory=list)
    
    # Venue specific
    venue_stats: Dict[str, Dict] = field(default_factory=dict)
    
    # Vs team specific
    vs_team_stats: Dict[str, Dict] = field(default_factory=dict)
    
    # Key moments involving this player
    key_moments: List[str] = field(default_factory=list)
    
    # Fantasy rating
    fantasy_rating: str = "B"  # S, A, B, C tier
    
    # Special traits
    special_traits: List[str] = field(default_factory=list)

@dataclass
class VenueInsight:
    """Ground characteristics and history"""
    venue_id: str
    name: str
    city: str
    
    # Pitch characteristics
    pitch_type: str
    avg_first_innings: int
    avg_second_innings: int
    chase_success_rate: str
    
    # Physical characteristics
    boundary_size: str
    dew_factor: str
    
    # Notable records
    highest_score: str
    lowest_score: str
    
    # Player favorites at this venue
    batting_favorites: Dict[str, str] = field(default_factory=dict)
    bowling_favorites: Dict[str, str] = field(default_factory=dict)
    
    # General behavior
    characteristics: List[str] = field(default_factory=list)

@dataclass
class FantasyScenario:
    """Decision-making scenarios for fantasy leagues"""
    scenario_id: str
    scenario_type: str  # captaincy, vice_captain, differential, toss_decision
    match_id: str
    match_name: str
    
    # Options to choose from
    options: List[str]
    
    # Recommendation
    recommendation: str
    reasoning: str
    
    # Alternative
    alternative: Optional[str] = None
    alternative_reasoning: Optional[str] = None
    
    # Context
    venue: str = ""
    match_situation: str = ""


# ==================== MATCH 1: RCB vs CSK ====================

MATCH_1_MOMENTS = [
    MatchMoment(
        moment_id="rcb_csk_001",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK, 11th Match, IPL 2026",
        over="16-20",
        event_type="finishing_blitz",
        description="Tim David unleashed absolute carnage in the death overs. After getting a reprieve when Anshul Kamboj bowled a no-ball, David smashed a 25-ball 70 not out with 8 sixes. One monstrous hit sailed 106 meters and landed on the Chinnaswamy roof. The crowd went wild as David and Patidar added 87 runs in just 32 balls.",
        players_involved=["Tim David", "Rajat Patidar", "Anshul Kamboj"],
        context="RCB was 163/3 after 16 overs, looking at 190-200. David's blitz propelled them to 250/3.",
        fantasy_impact="David owners received massive 98 points. Those who captained Patidar (48* off 19) got good returns but missed David's bonus.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-04-05"
    ),
    
    MatchMoment(
        moment_id="rcb_csk_002",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK, 11th Match, IPL 2026",
        over="10-15",
        event_type="counterattack",
        description="Sarfaraz Khan played a lone warrior innings for CSK. After the top order collapsed, the young batter counterattacked with a 24-ball fifty, including a six off Suyash Sharma that landed in the first tier at deep square-leg. His fighting spirit kept CSK's hopes alive briefly.",
        players_involved=["Sarfaraz Khan", "Suyash Sharma", "Krunal Pandya"],
        context="CSK was struggling at 45/3 chasing 250. Sarfaraz's 50 off 24 brought them back to 120/4.",
        fantasy_impact="Sarfaraz was a great differential pick, scoring 65 points. His aggressive approach surprised many who had benched him.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-04-05"
    ),
    
    MatchMoment(
        moment_id="rcb_csk_003",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK, 11th Match, IPL 2026",
        over="Powerplay",
        event_type="wickets",
        description="Jacob Duffy and Bhuvneshwar Kumar ripped through CSK's top order. Duffy got the dangerous Ruturaj Gaikwad early with a sharp inswinger. Bhuvi then removed both Devon Conway and Ajinkya Rahane in the same over with his trademark swing. CSK were reeling at 30/3.",
        players_involved=["Jacob Duffy", "Bhuvneshwar Kumar", "Ruturaj Gaikwad", "Devon Conway", "Ajinkya Rahane"],
        context="CSK chasing 250. Early wickets destroyed their chase momentum completely.",
        fantasy_impact="Bhuvneshwar's 3 wickets gave 75 points. Duffy's early breakthrough was crucial for fantasy teams.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-04-05"
    ),
    
    MatchMoment(
        moment_id="rcb_csk_004",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK, 11th Match, IPL 2026",
        over="15.3",
        event_type="missed_chance",
        description="Ruturaj Gaikwad later admitted in the post-match presentation that dropping Virat Kohli early was the turning point. Kohli was on 15 when he edged one to slip, but the chance went down. Kohli went on to score a steady 45 off 32, anchoring RCB's innings before the David-Patidar onslaught.",
        players_involved=["Virat Kohli", "Ruturaj Gaikwad"],
        context="Kohli on 15, RCB 45/1. The dropped catch proved fatal for CSK.",
        fantasy_impact="Gaikwad later admitted this cost CSK the match. Kohli's 45 runs after the drop proved decisive.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-04-05"
    ),
    
    MatchMoment(
        moment_id="rcb_csk_005",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK, 11th Match, IPL 2026",
        over="Middle overs",
        event_type="economical_spell",
        description="Suyash Sharma bowled a brilliant spell of 1/21 in 4 overs, the most economical of the match. His leg-spin tied down the CSK middle order. He removed the dangerous Sarfaraz Khan with a googly and kept the pressure on throughout.",
        players_involved=["Suyash Sharma", "Sarfaraz Khan"],
        context="CSK trying to rebuild at 120/4. Suyash's tight bowling prevented acceleration.",
        fantasy_impact="Suyash was a budget pick gem at 8 credits, giving 45 points with an economy bonus.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-04-05"
    )
]


# ==================== MATCH 3: SRH vs RCB (Season Opener) ====================

MATCH_3_MOMENTS = [
    MatchMoment(
        moment_id="srh_rcb_001",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB, 1st Match, IPL 2026",
        over="Powerplay",
        event_type="opening_spell",
        description="Jacob Duffy produced a sensational new-ball performance on his IPL debut. With the Chinnaswamy pitch offering spongy bounce and movement, Duffy removed Travis Head and Abhishek Sharma in his opening spell. Both batsmen were caught behind trying to drive. This twin strike reduced SRH to 20/2 and gave RCB early control.",
        players_involved=["Jacob Duffy", "Travis Head", "Abhishek Sharma", "Phil Salt"],
        context="SRH batting first. Duffy's 3 wickets in powerplay changed the entire match.",
        fantasy_impact="Duffy's dream debut gave 85 points. Taking Head and Abhishek - two explosive openers - was fantasy gold.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-03-23"
    ),
    
    MatchMoment(
        moment_id="srh_rcb_002",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB, 1st Match, IPL 2026",
        over="19.3",
        event_type="milestone",
        description="Virat Kohli became the FIRST batter in IPL history to cross 4000 runs in successful chases. He achieved this with a masterful 69 not out off 38 balls, including 4 fours and 3 sixes. The Chinnaswamy crowd gave him a standing ovation as he raised his bat. His last 5 scores against SRH read: 100, 42, 51, 43, 69*.",
        players_involved=["Virat Kohli"],
        context="RCB chasing 202. Kohli anchored the chase with another classic innings.",
        fantasy_impact="Kohli's consistency in chases makes him an S-tier captaincy option. 89 points this match.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-03-23"
    ),
    
    MatchMoment(
        moment_id="srh_rcb_003",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB, 1st Match, IPL 2026",
        over="8.2",
        event_type="catch",
        description="Phil Salt took a stunning one-handed catch diving to his right to dismiss Shivam Dube. The ball was traveling quickly off the edge, but Salt flew across and plucked it inches from the ground. This catch broke CSK's momentum and showcased Salt's wicketkeeping excellence.",
        players_involved=["Phil Salt", "Shivam Dube", "Krunal Pandya"],
        context="SRH rebuilding at 100/4. The catch triggered another collapse.",
        fantasy_impact="Salt's catch gave him 15 fielding points. His keeping skills add fantasy value beyond batting.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-03-23"
    ),
    
    MatchMoment(
        moment_id="srh_rcb_004",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB, 1st Match, IPL 2026",
        over="Powerplay",
        event_type="aggressive_batting",
        description="Devdutt Padikkal played an absolute blinder at the top of the order. He took on the SRH bowlers from ball one, smashing 48 off just 19 balls with 8 fours and 2 sixes. His aggressive approach allowed Kohli to play himself in. One shot over mid-on for six off a slower ball was particularly breathtaking.",
        players_involved=["Devdutt Padikkal", "Virat Kohli"],
        context="RCB chasing 202. Padikkal's blitz (48 off 19) set up the chase perfectly.",
        fantasy_impact="Padikkal's quickfire knock gave 72 points. Perfect example of a high-risk, high-reward differential pick.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-03-23"
    ),
    
    MatchMoment(
        moment_id="srh_rcb_005",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB, 1st Match, IPL 2026",
        over="15.4",
        event_type="record",
        description="RCB completed the chase of 202 in just 15.4 overs - the FASTEST 200-plus chase in IPL history! The previous record was RR vs GT in 2025 (15.5 overs). Virat Kohli finished with a flourish, hitting a six and two fours in the final over. This emphatic win sent a statement to the entire league.",
        players_involved=["Virat Kohli", "Tim David", "Devdutt Padikkal", "Rajat Patidar"],
        context="RCB chasing 202. They won with 26 balls to spare, breaking the IPL record.",
        fantasy_impact="All RCB batsmen gave massive points. This is why chasing at Chinnaswamy is fantasy heaven.",
        venue="Chinnaswamy Stadium, Bangalore",
        timestamp="2026-03-23"
    )
]


# ==================== MATCH 2: RCB vs MI (Partial Data) ====================

MATCH_2_MOMENTS = [
    MatchMoment(
        moment_id="rcb_mi_001",
        match_id="IPL2026_M20_RCBvMI",
        match_name="RCB vs MI, 20th Match, IPL 2026",
        over="17-20",
        event_type="wicket",
        description="Jacob Duffy removed the dangerous Hardik Pandya for 40 off 22 balls. Pandya was looking to accelerate MI's chase but lost his shape trying to slog a wide delivery outside off. The thick outside-edge flew to Romario Shepherd at deep backward point who took a comfortable catch. This wicket effectively sealed the match for RCB.",
        players_involved=["Jacob Duffy", "Hardik Pandya", "Romario Shepherd", "Krunal Pandya"],
        context="MI chasing. Hardik's wicket at this stage was the final nail in the coffin.",
        fantasy_impact="Duffy's wicket of Hardik was crucial - 25 points for the dismissal. Hardik's 40 gave 55 points before his dismissal.",
        venue="Wankhede Stadium, Mumbai",
        timestamp="2026-04-15"
    ),
    
    MatchMoment(
        moment_id="rcb_mi_002",
        match_id="IPL2026_M20_RCBvMI",
        match_name="RCB vs MI, 20th Match, IPL 2026",
        over="Middle overs",
        event_type="six_hitting",
        description="Sherfane Rutherford showcased his power-hitting abilities with a series of massive sixes. He deposited Suyash Sharma into the first tier at deep square-leg with a slog-sweep. Rutherford's quickfire 30 off 15 balls kept MI in the hunt briefly before the required rate climbed too high.",
        players_involved=["Sherfane Rutherford", "Suyash Sharma"],
        context="MI trying to chase down RCB's total. Rutherford's sixes brought temporary hope.",
        fantasy_impact="Rutherford's cameo gave 42 points. A good value pick for his strike rate.",
        venue="Wankhede Stadium, Mumbai",
        timestamp="2026-04-15"
    )
]


# Combine all moments
ALL_MOMENTS = MATCH_1_MOMENTS + MATCH_2_MOMENTS + MATCH_3_MOMENTS


# ==================== PLAYER PROFILES ====================

PLAYER_PROFILES = [
    PlayerProfile(
        player_id="virat_kohli",
        name="Virat Kohli",
        team="RCB",
        role="batsman",
        ipl_career_avg=48.5,
        ipl_strike_rate=138.2,
        matches_played=252,
        recent_form=[69, 45, 85, 42, 78],
        venue_stats={
            "Chinnaswamy Stadium": {"avg": 65.0, "matches": 85, "fifties": 25, "hundreds": 8},
            "Wankhede Stadium": {"avg": 48.0, "matches": 32, "fifties": 8, "hundreds": 2}
        },
        vs_team_stats={
            "CSK": {"avg": 52.0, "matches": 30},
            "MI": {"avg": 48.5, "matches": 35},
            "SRH": {"avg": 58.0, "matches": 20}
        },
        key_moments=[
            "First to 4000 runs in IPL chases",
            "69* (38) vs SRH in IPL 2026 opener",
            "Dropped catch by Gaikwad cost CSK dearly"
        ],
        fantasy_rating="S",
        special_traits=["Chase master", "Chinnaswamy specialist", "Consistent"]
    ),
    
    PlayerProfile(
        player_id="tim_david",
        name="Tim David",
        team="RCB",
        role="batsman",
        ipl_career_avg=35.0,
        ipl_strike_rate=175.0,
        matches_played=45,
        recent_form=[70, 35, 45, 25, 55],
        venue_stats={
            "Chinnaswamy Stadium": {"avg": 55.0, "matches": 12, "sixes_per_match": 4.5}
        },
        vs_team_stats={
            "CSK": {"avg": 62.0, "matches": 5}
        },
        key_moments=[
            "70* off 25 balls vs CSK with 8 sixes",
            "106m six onto Chinnaswamy roof",
            "87-run partnership with Patidar in 32 balls"
        ],
        fantasy_rating="A",
        special_traits=["Finisher", "Six-hitter", "Death overs specialist"]
    ),
    
    PlayerProfile(
        player_id="jacob_duffy",
        name="Jacob Duffy",
        team="RCB",
        role="bowler",
        ipl_career_avg=15.0,  # bowling avg
        ipl_strike_rate=18.0,  # balls per wicket
        matches_played=8,
        recent_form=[3, 2, 1, 4, 2],  # wickets
        venue_stats={
            "Chinnaswamy Stadium": {"wickets": 8, "avg": 18.0, "economy": 7.5}
        },
        vs_team_stats={
            "SRH": {"wickets": 3, "avg": 12.0},
            "MI": {"wickets": 2, "avg": 20.0}
        },
        key_moments=[
            "Dream IPL debut: 3 wickets vs SRH including Head and Abhishek",
            "Removed Hardik Pandya vs MI",
            "Player of the Match in IPL 2026 opener"
        ],
        fantasy_rating="A",
        special_traits=["New ball specialist", "Swing bowler", "Death overs"]
    ),
    
    PlayerProfile(
        player_id="rajat_patidar",
        name="Rajat Patidar",
        team="RCB",
        role="batsman",
        ipl_career_avg=42.0,
        ipl_strike_rate=155.0,
        matches_played=35,
        recent_form=[48, 65, 45, 72, 38],
        venue_stats={
            "Chinnaswamy Stadium": {"avg": 58.0, "matches": 20, "strike_rate": 165}
        },
        vs_team_stats={
            "CSK": {"avg": 55.0, "matches": 6}
        },
        key_moments=[
            "48* off 19 balls vs CSK, captain's knock",
            "Led RCB to 250 total with David",
            "RCB captain in IPL 2026"
        ],
        fantasy_rating="A",
        special_traits=["Captain", "Aggressive", "Finisher"]
    ),
    
    PlayerProfile(
        player_id="sarfaraz_khan",
        name="Sarfaraz Khan",
        team="CSK",
        role="batsman",
        ipl_career_avg=32.0,
        ipl_strike_rate=145.0,
        matches_played=25,
        recent_form=[50, 35, 28, 45, 22],
        venue_stats={
            "Chinnaswamy Stadium": {"avg": 38.0, "matches": 5}
        },
        vs_team_stats={
            "RCB": {"avg": 45.0, "matches": 4}
        },
        key_moments=[
            "Fighting 50 off 24 balls vs RCB",
            "Six off Suyash Sharma into first tier",
            "Lone warrior in CSK's chase of 250"
        ],
        fantasy_rating="B",
        special_traits=["Counter-attacker", "Middle order", "Differential pick"]
    ),
    
    PlayerProfile(
        player_id="bhuvneshwar_kumar",
        name="Bhuvneshwar Kumar",
        team="RCB",
        role="bowler",
        ipl_career_avg=26.0,
        ipl_strike_rate=21.0,
        matches_played=160,
        recent_form=[3, 2, 1, 2, 3],
        venue_stats={
            "Chinnaswamy Stadium": {"wickets": 45, "avg": 28.0, "economy": 8.0}
        },
        vs_team_stats={
            "CSK": {"wickets": 25, "avg": 24.0}
        },
        key_moments=[
            "3 wickets vs CSK including Conway and Rahane",
            "Swing bowling masterclass in powerplay",
            "Veteran death bowler for RCB"
        ],
        fantasy_rating="A",
        special_traits=["Swing bowler", "Death overs", "Economical"]
    ),
    
    PlayerProfile(
        player_id="devdutt_padikkal",
        name="Devdutt Padikkal",
        team="RCB",
        role="batsman",
        ipl_career_avg=38.0,
        ipl_strike_rate=140.0,
        matches_played=60,
        recent_form=[48, 55, 35, 62, 40],
        venue_stats={
            "Chinnaswamy Stadium": {"avg": 45.0, "matches": 25, "strike_rate": 150}
        },
        vs_team_stats={
            "SRH": {"avg": 52.0, "matches": 6}
        },
        key_moments=[
            "Blazing 48 off 19 balls vs SRH in IPL 2026 opener",
            "Set the tone for record chase",
            "World-class timing and balance"
        ],
        fantasy_rating="B",
        special_traits=["Aggressive opener", "Powerplay specialist"]
    ),
    
    PlayerProfile(
        player_id="hardik_pandya",
        name="Hardik Pandya",
        team="MI",
        role="all-rounder",
        ipl_career_avg=30.0,
        ipl_strike_rate=145.0,
        matches_played=120,
        recent_form=[40, 35, 28, 45, 32],
        venue_stats={
            "Wankhede Stadium": {"avg": 35.0, "matches": 40}
        },
        vs_team_stats={
            "RCB": {"avg": 32.0, "matches": 15}
        },
        key_moments=[
            "40 off 22 vs RCB before Duffy removed him",
            "Caught by Romario Shepherd at deep backward point",
            "MI captain trying to rescue chase"
        ],
        fantasy_rating="A",
        special_traits=["All-rounder", "Finisher", "Captain"]
    )
]


# ==================== VENUE INSIGHTS ====================

VENUE_INSIGHTS = [
    VenueInsight(
        venue_id="chinnaswamy",
        name="M. Chinnaswamy Stadium",
        city="Bangalore",
        pitch_type="Batting friendly",
        avg_first_innings=185,
        avg_second_innings=172,
        chase_success_rate="52%",
        boundary_size="55-60 meters (short)",
        dew_factor="High - helps chasing team",
        highest_score="263/5 by RCB vs PWI",
        lowest_score="92 all out by MI vs RCB",
        batting_favorites={
            "Virat Kohli": "Average 65, 8 centuries",
            "AB de Villiers": "Average 58, 2 centuries",
            "Chris Gayle": "Record 175*"
        },
        bowling_favorites={
            "Yuzvendra Chahal": "Spin works in middle overs",
            "Harshal Patel": "Death bowling specialist"
        },
        characteristics=[
            "True bounce and carry",
            "Short boundaries favor six-hitters",
            "Dew makes chasing easier",
            "High altitude - ball travels further",
            "Electric atmosphere for RCB games"
        ]
    ),
    
    VenueInsight(
        venue_id="wankhede",
        name="Wankhede Stadium",
        city="Mumbai",
        pitch_type="Balanced with pace bounce",
        avg_first_innings=175,
        avg_second_innings=168,
        chase_success_rate="48%",
        boundary_size="65-70 meters (medium)",
        dew_factor="Moderate",
        highest_score="235/9 by RCB vs MI",
        lowest_score="67 all out by KKR vs MI",
        batting_favorites={
            "Rohit Sharma": "Home ground specialist",
            "Suryakumar Yadav": "360-degree player"
        },
        bowling_favorites={
            "Jasprit Bumrah": "Yorker king at home"
        },
        characteristics=[
            "Red soil pitch - good bounce",
            "Evening sea breeze helps swing",
            "Fast outfield",
            "Good for both bat and ball"
        ]
    )
]


# ==================== FANTASY SCENARIOS ====================

FANTASY_SCENARIOS = [
    FantasyScenario(
        scenario_id="captaincy_001",
        scenario_type="captaincy",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK at Chinnaswamy",
        options=["Virat Kohli", "Rajat Patidar", "Tim David"],
        recommendation="Virat Kohli",
        reasoning="Kohli averages 65 at Chinnaswamy with 8 centuries. He's the chase master and has an incredible record against CSK at this venue. Consistent performer.",
        alternative="Tim David",
        alternative_reasoning="If you want a differential, David's death overs hitting can give explosive points. But riskier as he may not bat.",
        venue="Chinnaswamy Stadium",
        match_situation="RCB batting first or chasing"
    ),
    
    FantasyScenario(
        scenario_id="captaincy_002",
        scenario_type="captaincy",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB at Chinnaswamy",
        options=["Virat Kohli", "Devdutt Padikkal", "Rajat Patidar"],
        recommendation="Virat Kohli",
        reasoning="Chase master at his home ground. First game of season, fresh and hungry. 4000+ runs in chases - proven performer.",
        alternative="Devdutt Padikkal",
        alternative_reasoning="If batting first, Padikkal's aggressive powerplay approach can yield quick points. But Kohli is safer.",
        venue="Chinnaswamy Stadium",
        match_situation="RCB chasing 202"
    ),
    
    FantasyScenario(
        scenario_id="differential_001",
        scenario_type="differential",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK at Chinnaswamy",
        options=["Sarfaraz Khan", "Suyash Sharma", "Jacob Duffy"],
        recommendation="Sarfaraz Khan",
        reasoning="Low ownership, bats in middle order where runs needed. Can play counter-attacking knocks. Cheap pick with high upside.",
        alternative="Suyash Sharma",
        alternative_reasoning="Bowls in middle overs, economical, can pick wickets with variations. Good for economy bonus.",
        venue="Chinnaswamy Stadium",
        match_situation="CSK chasing big target"
    ),
    
    FantasyScenario(
        scenario_id="bowling_pick_001",
        scenario_type="bowling_pick",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK at Chinnaswamy",
        options=["Bhuvneshwar Kumar", "Jacob Duffy", "Yuzvendra Chahal"],
        recommendation="Bhuvneshwar Kumar",
        reasoning="Death overs specialist, swing bowler, proven at Chinnaswamy. Can bowl in powerplay and death - more overs = more points.",
        alternative="Jacob Duffy",
        alternative_reasoning="New ball specialist, in-form, wicket-taker. But might bowl fewer overs if expensive.",
        venue="Chinnaswamy Stadium",
        match_situation="RCB defending 250"
    ),
    
    FantasyScenario(
        scenario_id="toss_strategy_001",
        scenario_type="toss_decision",
        match_id="IPL2026_M11_RCBvCSK",
        match_name="RCB vs CSK at Chinnaswamy",
        options=["Bat first", "Chase"],
        recommendation="Chase",
        reasoning="Chinnaswamy has 52% chase success rate. Dew factor makes batting easier in second innings. Short boundaries mean no total is safe.",
        alternative="Bat first",
        alternative_reasoning="Only if you have strong batting lineup and want to put pressure. But chasing is statistically better.",
        venue="Chinnaswamy Stadium",
        match_situation="Toss time decision"
    ),
    
    FantasyScenario(
        scenario_id="finisher_pick_001",
        scenario_type="finisher",
        match_id="IPL2026_M1_SRHvRCB",
        match_name="SRH vs RCB at Chinnaswamy",
        options=["Tim David", "Dinesh Karthik", "MS Dhoni"],
        recommendation="Tim David",
        reasoning="RCB's designated finisher, bats at 5/6, can explode in death overs. 70* off 25 balls proved his capability.",
        alternative="Dinesh Karthik",
        alternative_reasoning="Experienced finisher, good behind wickets, but David has more explosive potential.",
        venue="Chinnaswamy Stadium",
        match_situation="Death overs specialist needed"
    )
]


# Helper functions
def get_all_moments() -> List[MatchMoment]:
    return ALL_MOMENTS

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
