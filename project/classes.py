import random


class Team:
    """
    Represents a baseball team, holding rosters for batters and pitchers.

    Attributes:
        code (str): The 3-letter abbreviation of the team used in the CSV files (e.g., "NYY").
        batters (list[Batter]): A list of Batter objects on the team.
        pitchers (list[Pitcher]): A list of Pitcher objects on the team.
        defense (float): The team's defensive rating (Runs Saved).
    """

    def __init__(self, code):
        """
        Initializes a new Team instance.

        :param code: The 3-letter team code (e.g., 'BOS').
        :type code: str
        """
        self.code = code
        self.batters = []
        self.pitchers = []
        self.defense = 0.0

    # Adds Batters
    def add_batter(self, batter):
        """
        Adds a Batter object to the team's roster.

        :param batter: The Batter object to add.
        :type batter: Batter
        """
        self.batters.append(batter)

    # Adds Pitchers
    def add_pitcher(self, pitcher):
        """
        Adds a Pitcher object to the team's roster.

        :param pitcher: The Pitcher object to add.
        :type pitcher: Pitcher
        """
        self.pitchers.append(pitcher)

    # Get best 3 Pitchers, select 1
    def get_starting_pitcher(self):
        """
        Selects a starting pitcher from the team's top 3 pitchers.

        Sorts all pitchers by 'overall' rating, takes the top 3, and randomly
        selects one to simulate rotation variance.

        :return: A Pitcher object, or None if no pitchers exist.
        :rtype: Pitcher | None
        """
        if not self.pitchers:
            return None
        sorted_pitchers = sorted(self.pitchers, key=lambda p: p.overall, reverse=True)
        top3_pitchers = sorted_pitchers[:3]
        return random.choice(top3_pitchers)

    # Get best 9 batters
    def get_starting_lineup(self):
        """
        Returns the best 9 batters sorted by overall rating.

        :return: A list of the top 9 Batter objects.
        :rtype: list[Batter]
        """
        if len(self.batters) < 9:
            return self.batters
        best_batters = sorted(self.batters, key=lambda p: p.overall, reverse=True)
        return best_batters[:9]


class Pitcher:
    """
    Represents a single Pitcher with stats from the 2025 season.
    """

    def __init__(self, stats):
        """
        Parses a dictionary of stats to initialize a Pitcher.

        Calculates an 'overall' rating based on WAR, ERA, and WHIP using a
        weighted formula prioritizing WAR and ERA.

        :param stats: A dictionary containing raw CSV row data.
        :type stats: dict
        """
        # Pitcher Name and Team
        self.name = stats["Player"].strip("*#").strip()
        self.team = stats["Team"]

        # Pitcher Stats
        try:
            self.era = float(stats["ERA"])
            self.whip = float(stats["WHIP"])
            self.war = float(stats["WAR"])
        except ValueError:
            self.era = 99.99
            self.whip = 99.99
            self.war = 0.0

        # Pitcher Overall
        self.overall = (
            50 + (3 * self.war) + 8 * (5.5 - self.era) + 20 * (1.5 - self.whip)
        )


class Batter:
    """
    Represents a single Batter with stats from the 2025 season.
    """

    def __init__(self, stats):
        """
        Parses a dictionary of stats to initialize a Batter.

        Calculates an 'overall' rating based on WAR and OPS.

        :param stats: A dictionary containing raw CSV row data.
        :type stats: dict
        """
        # Batter Name and Team
        self.name = stats["Player"].strip("*#").strip()
        self.team = stats["Team"]

        # Batter Stats
        try:
            self.ops = float(stats["OPS"])
            self.war = float(stats["WAR"])
            self.obp = float(stats["OBP"])
            self.slg = float(stats["SLG"])
        except ValueError:
            self.ops = 0.0
            self.war = 0.0
            self.obp = 0.0
            self.slg = 0.0

        # Batter Overall
        self.overall = 50 + (3 * self.war) + (25 * self.ops)