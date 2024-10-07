import json
from uade_battleship.utils import FileStorage
from .match_data import MatchCellState, Coord, MatchData, PlayerData, ShipPosition

BOARD_SIZE = 10


class Match:
    match_data: MatchData

    def __init__(
        self, player_1_name: str = "Player 1", player_2_name: str = "Player 2"
    ):
        self.match_data = MatchData(
            type="singleplayer",
            player_1=PlayerData(name=player_1_name, fleet=[], shots_received=[]),
            player_2=PlayerData(name=player_2_name, fleet=[], shots_received=[]),
        )

    def get_players(self) -> tuple[str, str]:
        return self.match_data["player_1"]["name"], self.match_data["player_2"]["name"]

    def add_shot(self, player_shot: int, coord: Coord):
        player_data = (
            self.match_data["player_1"]
            if player_shot == 1
            else self.match_data["player_2"]
        )

        # Check if shot has already been made
        if coord in player_data["shots_received"]:
            raise ValueError("Shot has already been made")

        # Check if shot is within bounds
        if (
            coord["x"] < 0
            or coord["x"] >= BOARD_SIZE
            or coord["y"] < 0
            or coord["y"] >= BOARD_SIZE
        ):
            raise ValueError("Shot is out of bounds")

        player_data["shots_received"].append(coord)

    def add_ship(self, player: int, ship: ShipPosition):
        player_data = (
            self.match_data["player_1"] if player == 1 else self.match_data["player_2"]
        )

        # Check if ship is within bounds
        if ship["orientation"] == "horizontal":
            if ship["x"] + ship["size"] > BOARD_SIZE:
                raise ValueError("Ship is out of bounds")
        else:
            if ship["y"] + ship["size"] > BOARD_SIZE:
                raise ValueError("Ship is out of bounds")

        # Check that ship does not overlap with other ships
        for other_ship in player_data["fleet"]:
            if ship["orientation"] == "horizontal":
                if (
                    ship["y"] == other_ship["y"]
                    and ship["x"] < other_ship["x"] + other_ship["size"]
                    and ship["x"] + ship["size"] > other_ship["x"]
                ):
                    raise ValueError("Ship overlaps with other ship")
            else:
                if (
                    ship["x"] == other_ship["x"]
                    and ship["y"] < other_ship["y"] + other_ship["size"]
                    and ship["y"] + ship["size"] > other_ship["y"]
                ):
                    raise ValueError("Ship overlaps with other ship")

        player_data["fleet"].append(ship)

    def get_board(self, player: int) -> list[list[MatchCellState]]:
        board = [
            [MatchCellState.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        player_data = (
            self.match_data["player_1"] if player == 1 else self.match_data["player_2"]
        )

        for ship in player_data["fleet"]:
            if ship["orientation"] == "horizontal":
                for i in range(ship["size"]):
                    board[ship["y"]][ship["x"] + i] = MatchCellState.SHIP
            else:
                for i in range(ship["size"]):
                    board[ship["y"] + i][ship["x"]] = MatchCellState.SHIP

        for coord in player_data["shots_received"]:
            x, y = coord["x"], coord["y"]
            if board[y][x] == MatchCellState.SHIP:
                board[y][x] = MatchCellState.HIT
            else:
                board[y][x] = MatchCellState.MISS

        return board

    def get_json(self) -> str:
        return json.dumps(self.match_data, indent=2)

    def save(self):
        match_data_json = self.get_json()
        FileStorage.write_file("match.json", match_data_json)

    @staticmethod
    def from_json(data: str) -> "Match":
        match_data = json.loads(data)
        match = Match()
        match.match_data.update(match_data)
        return match
