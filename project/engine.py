import random


class Engine:
    """
    The core Sabermetric engine for the MLB Replay Simulator.

    Manages the game state including score, innings, outs, and baserunners.
    Implements the Sabermetric algorithms for determining at-bat outcomes.
    """

    def __init__(self, home_team, away_team, home_pitcher, away_pitcher):
        """
        Initializes the Game Engine with teams and starting pitchers
        The Pitcher is initialized here to avoid getting 2 different pitchers.

        :param home_team: The Home Team object.
        :param away_team: The Away Team object.
        :param home_pitcher: The starting Pitcher for the home team.
        :param away_pitcher: The starting Pitcher for the away team.
        """
        self.home_team = home_team
        self.away_team = away_team
        self.home_pitcher = home_pitcher
        self.away_pitcher = away_pitcher
        self.home_score = 0
        self.away_score = 0
        self.inning = 1

        self.home_pitcher_fatigue = 0.0
        self.away_pitcher_fatigue = 0.0

    def play(self):
        """
        Starts the main game loop.

        Loops through innings until 9 innings are complete and the score is not tied.
        Increases pitcher fatigue after every inning to simulate stamina loss.
        Prevent the game from going beyond the 15 innings limit.
        """
        print(f"\n ⚾ PLAY BALL! {self.away_team.code} vs {self.home_team.code} ⚾")
        print(
            f"   Pitching Matchup: {self.away_pitcher.name} vs {self.home_pitcher.name}\n"
        )

        while self.inning <= 9 or self.away_score == self.home_score:
            if self.inning > 15:
                print("\n   ⚠️ GAME CALLED (15 Innings limit) ⚠️")
                break

            self.play_inning()

            self.home_pitcher_fatigue += 0.05
            self.away_pitcher_fatigue += 0.05

            self.inning += 1

        self.declare_winner()

    def play_inning(self):
        """
        Simulates a single full inning (Top and Bottom).

        Handles the logic for "Walk-offs" (if Home team leads in bottom of 9th).
        """
        print(f"--- Top of the {self.inning} ---")
        self.play_half_inning(
            self.away_team,
            self.home_team,
            self.home_pitcher,
            self.home_pitcher_fatigue,
            is_home=False,
        )

        if self.inning >= 9 and self.home_score > self.away_score:
            return

        print(f"--- Bottom of the {self.inning} ---")
        self.play_half_inning(
            self.home_team,
            self.away_team,
            self.away_pitcher,
            self.away_pitcher_fatigue,
            is_home=True,
        )

        print(
            f"   [SCORE] {self.away_team.code}: {self.away_score} | {self.home_team.code}: {self.home_score}\n"
        )

    def play_half_inning(self, batting_team, defending_team, pitcher, fatigue, is_home):
        """
        Simulates one half-inning of baseball.

        Iterates through the batting lineup until 3 outs are recorded.

        :param batting_team: The Team currently at bat.
        :param defending_team: The Team currently in the field.
        :param pitcher: The Pitcher currently on the mound.
        :param fatigue: The current fatigue modifier for the pitcher.
        :param is_home: Boolean indicating if the batting team is the Home team.
        """
        outs = 0
        bases = [0, 0, 0]

        lineup = batting_team.get_starting_lineup()

        if not hasattr(batting_team, "current_batter_index"):
            batting_team.current_batter_index = 0

        while outs < 3:
            if self.inning >= 9 and is_home and self.home_score > self.away_score:
                break

            batter = lineup[batting_team.current_batter_index]

            result = self.simulate_at_bat(
                batter, pitcher, defending_team.defense, fatigue
            )

            if result == "OUT":
                outs += 1
            elif result == "WALK":
                print(f"  🚶 {batter.name} walks.")
                self.advance_runners(bases, hits=1, is_walk=True, is_home=is_home)
            elif result == "SINGLE":
                print(f"  ⚾ {batter.name} singles.")
                self.advance_runners(bases, hits=1, is_walk=False, is_home=is_home)
            elif result == "DOUBLE":
                print(f"  ⚡ {batter.name} hits a DOUBLE!")
                self.advance_runners(bases, hits=2, is_walk=False, is_home=is_home)
            elif result == "TRIPLE":
                print(f"  🔥 {batter.name} hits a TRIPLE!")
                self.advance_runners(bases, hits=3, is_walk=False, is_home=is_home)
            elif result == "HR":
                print(f"  🚀 HOME RUN!! {batter.name} goes deep!")
                runs = sum(bases) + 1
                if is_home:
                    self.home_score += runs
                else:
                    self.away_score += runs
                bases = [0, 0, 0]

            batting_team.current_batter_index = (
                batting_team.current_batter_index + 1
            ) % 9

    def advance_runners(self, bases, hits, is_walk, is_home):
        """
        Calculates runner movement and scoring based on the type of hit.

        Updates the `bases` list in-place and updates the score attributes.

        :param bases: List of length 3 representing [1st, 2nd, 3rd]. 1=Occupied, 0=Empty.
        :param hits: Integer representing bases gained (1=Single/Walk, 2=Double, etc).
        :param is_walk: Boolean, if True, applies force-movement logic only.
        :param is_home: Boolean, determines which score to increment.
        """
        runs_scored = 0

        if is_walk:
            if bases[0] == 1:
                if bases[1] == 1:
                    if bases[2] == 1:
                        runs_scored += 1
                    bases[2] = 1
                bases[1] = 1
            bases[0] = 1
        else:
            if bases[2] == 1:
                runs_scored += 1
                bases[2] = 0

            if bases[1] == 1:
                if hits >= 2:
                    runs_scored += 1
                    bases[1] = 0
                else:
                    bases[2] = 1
                    bases[1] = 0

            if bases[0] == 1:
                if hits == 3:
                    runs_scored += 1
                    bases[0] = 0
                elif hits == 2:
                    bases[2] = 1
                    bases[0] = 0
                else:
                    bases[1] = 1
                    bases[0] = 0

            if hits == 1:
                bases[0] = 1
            elif hits == 2:
                bases[1] = 1
            elif hits == 3:
                bases[2] = 1

        if runs_scored > 0:
            print(f"  ✨ {runs_scored} run(s) scored!")
            if is_home:
                self.home_score += runs_scored
            else:
                self.away_score += runs_scored

    def simulate_at_bat(self, batter, pitcher, defense_rating, fatigue):
        """
        Determines the outcome of an at-bat using Sabermetric probabilities.

        Comparing Batter OBP vs Pitcher WHIP (adjusted for fatigue).
        If contact is made, checks against defensive rating.
        Finally, determines hit type based on probabilities and ISO power.

        :param batter: The Batter object at the plate.
        :param pitcher: The Pitcher object on the mound.
        :param defense_rating: The defensive rating (Rdrs) of the fielding team.
        :param fatigue: The fatigue modifier adding to the pitcher's WHIP.
        :return: String representing outcome ("OUT", "SINGLE", "HR", etc).
        :rtype: str
        """
        AVG_WHIP = 1.30 # Common number for the MLB average WHIP
        WHIP_COEFF = 0.40 # Dampener
        DEFENSE_DIVISOR = 300 # Don't make defenses OP

        # MLB OBP average is .315 and Walk Rate is ~.080 = .250 on-base events are walks
        WALK_RATE = 0.225
        # 53% of on-base events are Singles (.530 + .225)
        SINGLE_RATE = 0.755
        XBH_RATE = 0.92
        TRIPLE_CHANCE = 0.15

        # Power Scaling
        ISO_MULTIPLIER = 2.5

        # 1. CALCULATE CONTACT CHANCE
        current_whip = pitcher.whip + fatigue
        whip_diff = current_whip - AVG_WHIP

        # Apply the coefficient to dampen the impact of extreme pitching stats
        adjusted_obp = batter.obp + (whip_diff * WHIP_COEFF)
        adjusted_obp = max(0.100, min(0.700, adjusted_obp))

        if random.random() > adjusted_obp:
            return "OUT"

        # 2. DEFENSE CHECK
        defense_save_chance = max(0, defense_rating / DEFENSE_DIVISOR)
        if random.random() < defense_save_chance:
            print(f"  🛡️ ROBBED! Great play by the {pitcher.team} defense!")
            return "OUT"

        # 3. DETERMINE HIT TYPE
        type_roll = random.random()

        if type_roll < WALK_RATE:
            return "WALK"

        elif type_roll < SINGLE_RATE:
            return "SINGLE"

        elif type_roll < XBH_RATE:
            return "TRIPLE" if random.random() < TRIPLE_CHANCE else "DOUBLE"

        else:
            # 4. POWER CHECK (Home Run vs Wall Ball)
            iso = batter.ops - batter.obp
            # Calculate how easy it is for this specific batter to hit a HR
            power_threshold = 1.0 - (iso * ISO_MULTIPLIER)

            if random.random() > power_threshold:
                return "HR"
            else:
                return "DOUBLE"

    def declare_winner(self):
        """
        Prints the final score and declares the winner.
        """
        print("=" * 40)
        print("         FINAL SCORE")
        print("=" * 40)
        print(f" {self.away_team.code}: {self.away_score}")
        print(f" {self.home_team.code}: {self.home_score}")
        if self.home_score > self.away_score:
            print(f"🏆 {self.home_team.code} WINS! 🏆")
        elif self.away_score > self.home_score:
            print(f"🏆 {self.away_team.code} WINS! 🏆")
        else:
            print("It's a TIE!")