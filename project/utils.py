import csv

from classes import Batter, Pitcher, Team

# Team Info
# Key: Team Code -> Value: [Team Full Name, 2025 Stadium Name]
TEAM_INFO = {
    "ARI": ["Arizona Diamondbacks", "Chase Field"],
    "ATH": ["Athletics", "Sutter Health Park"],
    "ATL": ["Atlanta Braves", "Truist Park"],
    "BAL": ["Baltimore Orioles", "Camden Yards"],
    "BOS": ["Boston Red Sox", "Fenway Park"],
    "CHC": ["Chicago Cubs", "Wrigley Field"],
    "CHW": ["Chicago White Sox", "Guaranteed Rate Field"],
    "CIN": ["Cincinnati Reds", "Great American Ball Park"],
    "CLE": ["Cleveland Guardians", "Progressive Field"],
    "COL": ["Colorado Rockies", "Coors Field"],
    "DET": ["Detroit Tigers", "Comerica Park"],
    "HOU": ["Houston Astros", "Minute Maid Park"],
    "KCR": ["Kansas City Royals", "Kauffman Stadium"],
    "LAA": ["Los Angeles Angels", "Angel Stadium"],
    "LAD": ["Los Angeles Dodgers", "Dodger Stadium"],
    "MIA": ["Miami Marlins", "LoanDepot Park"],
    "MIL": ["Milwaukee Brewers", "American Family Field"],
    "MIN": ["Minnesota Twins", "Target Field"],
    "NYM": ["New York Mets", "Citi Field"],
    "NYY": ["New York Yankees", "Yankee Stadium"],
    "PHI": ["Philadelphia Phillies", "Citizens Bank Park"],
    "PIT": ["Pittsburgh Pirates", "PNC Park"],
    "SDP": ["San Diego Padres", "Petco Park"],
    "SEA": ["Seattle Mariners", "T-Mobile Park"],
    "SFG": ["San Francisco Giants", "Oracle Park"],
    "STL": ["St. Louis Cardinals", "Busch Stadium"],
    "TBR": ["Tampa Bay Rays", "Steinbrenner Field"],
    "TEX": ["Texas Rangers", "Globe Life Field"],
    "TOR": ["Toronto Blue Jays", "Rogers Centre"],
    "WSN": ["Washington Nationals", "Nationals Park"],
}


def load_all_batters(filename):
    """
    Parses a CSV file to create a list of Batter objects.

    :param filename: The path to the CSV file containing batting statistics.
    :type filename: str
    :return: A list of initialized Batter objects.
    :rtype: list[Batter]
    """
    all_batters = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_batter = Batter(row)
            all_batters.append(new_batter)
    return all_batters


def load_all_pitchers(filename):
    """
    Parses a CSV file to create a list of Pitcher objects.

    Filters out pitchers who have pitched fewer than 20 innings to avoid
    loading position players or rarely used relievers.

    :param filename: The path to the CSV file containing pitching statistics.
    :type filename: str
    :return: A list of initialized Pitcher objects.
    :rtype: list[Pitcher]
    """
    all_pitchers = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                ip = float(row.get("IP", 0))
            except ValueError:
                ip = 0.0

            if ip > 20.0:  # Only load pitchers with > 20 Innings Pitched
                new_pitcher = Pitcher(row)
                all_pitchers.append(new_pitcher)

    return all_pitchers


def create_league(batters, pitchers):
    """
    Organizes batters and pitchers into Team objects keyed by their team code.

    Iterates through lists of players and assigns them to the appropriate Team
    object in a dictionary. Creates new Team objects as needed.

    :param batters: A list of Batter objects.
    :type batters: list[Batter]
    :param pitchers: A list of Pitcher objects.
    :type pitchers: list[Pitcher]
    :return: A dictionary mapping team codes (str) to Team objects.
    :rtype: dict
    """
    league = {}

    for batter in batters:
        code = batter.team
        if not code or code.endswith("TM"):
            continue
        if code not in league:
            league[code] = Team(code)
        league[code].add_batter(batter)

    for pitcher in pitchers:
        code = pitcher.team
        if not code or code.endswith("TM"):
            continue
        if code not in league:
            league[code] = Team(code)
        league[code].add_pitcher(pitcher)

    return league


def load_defense(filename, league):
    """
    Loads defensive statistics from a CSV file and updates existing Team objects.

    Updates the 'defense' attribute (Rdrs) of teams found in the league dictionary
    in-place.

    :param filename: The path to the CSV file containing fielding statistics.
    :type filename: str
    :param league: The dictionary containing Team objects to be updated.
    :type league: dict
    :return: None
    """
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_code = row["Team"]
            try:
                runs_saved = float(row["Rdrs"])
            except ValueError:
                runs_saved = 0.0
            if team_code in league:
                league[team_code].defense += runs_saved