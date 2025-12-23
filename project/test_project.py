import pytest
from project import get_team_object, format_matchup_header, load_league_data
from classes import Team


# 1. Test get_team_object
def test_get_team_object():
    # Create a fake league dictionary
    fake_league = {
        "NYY": Team("NYY"),
        "BOS": Team("BOS")
    }

    # Test valid input
    result = get_team_object(fake_league, "nyy")  # Lowercase input check
    assert result is not None
    assert result.code == "NYY"

    # Test invalid input
    result = get_team_object(fake_league, "LAD")
    assert result is None


# 2. Test format_matchup_header
def test_format_matchup_header():
    away = "Yankees"
    home = "Red Sox"
    stadium = "Fenway"

    expected_snippet = "MATCHUP SET: Yankees @ Red Sox"

    result = format_matchup_header(away, home, stadium)

    assert expected_snippet in result
    assert "VENUE: Fenway" in result
    assert "=" * 60 in result


# 3. Test load_league_data
def test_load_league_data():
    # This test attempts to load the ACTUAL files.
    # It ensures the data pipeline is connected correctly.
    try:
        league = load_league_data()

        # Check if league is a dictionary
        assert isinstance(league, dict)

        # Check if the contents are Team objects
        first_key = list(league.keys())[0]
        assert isinstance(league[first_key], Team)

    except FileNotFoundError:
        pytest.fail("Data files missing. Cannot test load_league_data.")