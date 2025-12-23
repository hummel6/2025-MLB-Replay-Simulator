import sys
from utils import (
    load_all_batters,
    load_all_pitchers,
    load_defense,
    create_league,
    TEAM_INFO,
)
from engine import Engine


def main():
    """
    The main entry point for the MLB Replay Simulator.

    Orchestrates the flow of the application:
    1. Loads data from the CSV files.
    2. Displays available teams.
    3. Handles user input for team selection.
    4. Initializes and runs the simulation engine.
    """
    # 1. Welcome Message
    print("\n" + "=" * 40)
    print("         ⚾ MLB REPLAY SIMULATOR ⚾ ")
    print("=" * 40 + "\n")
    print("Loading 2025 data...")

    # 2. Load Data
    try:
        league = load_league_data()
    except FileNotFoundError:
        sys.exit("Critical Error: CSV data files not found in 'data/' folder.")

    print(f"✔ League Loaded: {len(league)} Teams ready.\n")

    # 3. Display Teams
    display_available_teams(league)

    # 4. Team Selection
    print("=== SELECT MATCHUP ===")

        # Input Loop for Away Team
    while True:
        code_input = input("Enter AWAY Team Code: (e.g. NYY)\n> ").strip()
        away_team = get_team_object(league, code_input)
        if away_team:
            break
        print(f"ERROR: '{code_input}' is not a valid team code.")

        # Input Loop for Home Team
    while True:
        code_input = input("Enter HOME Team Code: (e.g. BOS)\n> ").strip()
        home_team = get_team_object(league, code_input)
        if home_team:
            break
        print(f"ERROR: '{code_input}' is not a valid team code.")

    # 5. Match Info
    away_full = TEAM_INFO.get(away_team.code, [away_team.code, "Unknown"])[0]
    home_full_stats = TEAM_INFO.get(home_team.code, [home_team.code, "Unknown"])
    home_full = home_full_stats[0]
    stadium = home_full_stats[1]

    header = format_matchup_header(away_full, home_full, stadium)
    print(header)

    # 6. Select Pitchers
    away_pitcher = away_team.get_starting_pitcher()
    home_pitcher = home_team.get_starting_pitcher()

    # 7. Print Lineups
    print_team_summary(away_team, away_full, "AWAY", away_pitcher)
    print_team_summary(home_team, home_full, "HOME", home_pitcher)

    input("\nPress Enter to start simulation...")

    # 8. Start Engine
    sim = Engine(home_team, away_team, home_pitcher, away_pitcher)
    sim.play()


def load_league_data():
    """
    Loads all necessary data from the CSV files and constructs the league structure.

    Orchestrates the loading of batters, pitchers, and defensive stats from
    the 'data/' directory using functions from utils.py.

    :return: A dictionary where keys are the team codes (str) and values are Team objects.
    :rtype: dict
    """
    batters = load_all_batters("data/batting_2025.csv")
    pitchers = load_all_pitchers("data/pitching_2025.csv")
    league = create_league(batters, pitchers)
    load_defense("data/fielding_2025.csv", league)
    return league


def get_team_object(league, code):
    """
    Retrieves a Team object from the league dictionary based on the code provided by the user.

    Case-insensitive. Returns None if the team code does not exist.

    :param league: The dictionary containing all Team objects.
    :type league: dict
    :param code: The 3-letter team abbreviation input by the user.
    :type code: str
    :return: The Team object if the code exists, otherwise None.
    :rtype: Team | None
    """
    code = code.upper().strip()
    if code in league:
        return league[code]
    return None


def format_matchup_header(away_name, home_name, stadium_name):
    """
    Returns a formatted string containing the matchup details and venue.

    :param away_name: The full name of the away team.
    :type away_name: str
    :param home_name: The full name of the home team.
    :type home_name: str
    :param stadium_name: The name of the stadium where the game is played.
    :type stadium_name: str
    :return: A multi-line string formatted for display in the console.
    :rtype: str
    """
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append(f" ⚾ MATCHUP SET: {away_name} @ {home_name}")
    lines.append(f" 🏟  VENUE: {stadium_name}")
    lines.append("=" * 60)
    return "\n".join(lines)


def display_available_teams(league):
    """
    Prints a formatted list of all available teams in the league to the console.

    Iterates through the league keys, retrieves full names from TEAM_INFO,
    and prints them in a two-column format.

    :param league: The dictionary containing all Team objects.
    :type league: dict
    :return: None
    """
    print("\n" + "=" * 50)
    print(f"             ⚾ AVAILABLE TEAMS ({len(league)}) ⚾")
    print("=" * 50)
    sorted_codes = sorted(league.keys())
    for i in range(0, len(sorted_codes), 2):
        code_1 = sorted_codes[i]
        name_1 = TEAM_INFO.get(code_1, [code_1])[0]
        if i + 1 < len(sorted_codes):
            code_2 = sorted_codes[i + 1]
            name_2 = TEAM_INFO.get(code_2, [code_2])[0]
            print(f"[{code_1}] {name_1:<25} | [{code_2}] {name_2}")
        else:
            print(f"[{code_1}] {name_1}")
    print("=" * 50 + "\n")


def print_team_summary(team, full_name, label, pitcher_obj):
    """
    Prints a detailed summary of a team's lineup and starting pitcher.

    :param team: The Team object containing roster data.
    :type team: Team
    :param full_name: The full name of the team (e.g., "New York Yankees").
    :type full_name: str
    :param label: The designation of the team (e.g., "HOME" or "AWAY").
    :type label: str
    :param pitcher_obj: The Pitcher object selected to start the game.
    :type pitcher_obj: Pitcher
    :return: None
    """
    print(f"\n--- {label}: {full_name} ---")
    if pitcher_obj:
        print(f"Starting Pitcher: {pitcher_obj.name} (Rating: {pitcher_obj.overall:.1f})")
    else:
        print(f"Starting Pitcher: N/A")
    print(f"Defense Rating:   {team.defense:.1f}")
    print("Lineup:")
    for i, batter in enumerate(team.get_starting_lineup(), 1):
        print(f"  {i}. {batter.name:<20} (Rat: {batter.overall:.1f})")


if __name__ == "__main__":
    main()