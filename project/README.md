# ⚾ 2025 MLB Replay Simulator

#### Video Demo:  <https://youtu.be/n_sNASj1H00>

#### Description:
The **MLB Replay Simulator** is a terminal-based Python application that _tries_ to simulate realistic baseball games using 2025 season real player data. Unlike simple random number generators, this simulation uses a **Sabermetric Engine** that calculates outcomes based on real baseball statistics (OBP, WHIP, ERA, OPS, and Defensive Data).

The user can select any two MLB teams that played the 2025, and the program will generate a play-by-play simulation of a 9-inning game (with extra innings if necessary), displaying live scores, play descriptions, and a final box score.

### Project Structure

The project is organized into four main Python files:

1.  **`project.py`**:
    * The entry point of the application.
    * Handles User Interface (UI), inputs, and the high-level flow.
    * Orchestrates data loading and initializes the simulation.


2.  **`engine.py`**:
    * Contains the `Engine` class, which manages the game state (score, innings, outs, runners on base).
    * **Key Feature**: Contains the `simulate_at_bat` algorithm that pits a Batter's stats against a Pitcher's stats, applies Defensive modifiers, and determines the outcome using probability buckets.


3.  **`classes.py`**:
    * Defines the data models: `Team`, `Batter`, and `Pitcher`.
    * Calculates the "Overall Rating" for players using weighted formulas (e.g., heavily weighting WAR and ERA for pitchers).
    * Manages roster logic, such as sorting lineups by best players.
    * Selects a random top 3 pitcher from the selected team


4.  **`utils.py`**:
    * Handles all File I/O operations.
    * Parses the CSV files in the `data/` folder.
    * Includes logic to filter out non-pitchers (position players who pitched 1 inning) to ensure simulation quality.

### Design Choices

#### The Simulation Engine
Instead of simple dice rolls, I implemented a comparative algorithm. The engine calculates an **Adjusted OBP** (On-Base Percentage) by comparing the Batter's OBP against the Pitcher's WHIP (Walks plus Hits per Inning Pitched).
* *Why?* This ensures that an Ace pitcher (like Garrett Crochet) dominates average hitters, but great hitters (like Aaron Judge) can still succeed against him.

#### Pitcher Fatigue
I noticed early in testing that Closing Pitchers were too dominant in the late innings.
* *Solution:* I implemented a `fatigue` variable in `engine.py`. Every inning, the pitcher's effective WHIP increases by 0.05. This naturally simulates a pitcher getting tired and makes late-game comebacks possible, making the simulation more dynamic.

#### Defensive Rating
To make the game feel dynamic, I integrated the team's "Rdrs" (Defensive Runs Saved) stat.
* *Implementation:* Even if the math says a "Hit" occurred, the engine rolls a final check against the defensive rating. A high-defense team has a higher % chance to "Rob" a hit, turning it into an Out.

#### Base Running Logic
Early versions of the game simply counted hits to score runs. This felt arcade-like.
* *Improvement:* I implemented a list `bases = [0, 0, 0]` representing 1st, 2nd, and 3rd base, respectively. The `advance_runners` function now mathematically moves runners based on the hit type (e.g., a Single moves a runner from 1st to 2nd, but a Double scores him).

### Installation & Usage

1.  **Prerequisites:** Python 3 and `pip`.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The only external dependency is `pytest` for testing. The game itself uses standard libraries.)*
3.  **Run the Game:**
    ```bash
    python project.py
    ```
4.  **Run Tests:**
    ```bash
    pytest test_project.py
    ```

### Data Sources
The game uses 2025 real data (CSV format) located in the `data/` folder:
* `batting_2025.csv`
* `pitching_2025.csv`
* `fielding_2025.csv`

All the data used is possible thanks to Baseball Reference. (<https://www.baseball-reference.com/>)