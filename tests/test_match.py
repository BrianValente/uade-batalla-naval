import json
from uade_battleship.match import Match, MatchCellState


def test_new_match():
    match = Match("Player 1", "Player 2")
    players = match.get_players()
    assert players == ("Player 1", "Player 2")
    assert match.get_board(1)[0][0] == MatchCellState.EMPTY

    match.add_ship(0, {"x": 0, "y": 0, "size": 3, "orientation": "horizontal"})
    match.add_ship(1, {"x": 0, "y": 0, "size": 3, "orientation": "vertical"})
    assert match.get_board(1)[0][0] == MatchCellState.SHIP

    match.add_shot(0, {"x": 0, "y": 0})
    match.add_shot(1, {"x": 0, "y": 0})
    assert match.get_board(1)[0][0] == MatchCellState.HIT


def test_loaded_match():
    match_1 = Match("Player 1", "Player 2")
    match_1.add_ship(0, {"x": 0, "y": 0, "size": 3, "orientation": "horizontal"})
    match_1.add_shot(0, {"x": 0, "y": 0})
    json_data = match_1.get_json()
    match_2 = Match.from_json(json_data)
    assert match_1.get_players() == match_2.get_players()
    assert json.dumps(match_1.get_board(1)) == json.dumps(match_2.get_board(1))


def test_out_of_bounds_ship():
    match = Match("Player 1", "Player 2")
    try:
        match.add_ship(0, {"x": 8, "y": 0, "size": 3, "orientation": "horizontal"})
        assert False
    except ValueError:
        assert True


def test_out_of_bounds_shot():
    match = Match("Player 1", "Player 2")
    try:
        match.add_shot(0, {"x": 10, "y": 0})
        assert False
    except ValueError:
        assert True
