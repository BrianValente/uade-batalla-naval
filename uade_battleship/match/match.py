import json
from typing import TypedDict
from uade_battleship.utils import FileStorage
from .match_data import (
    MatchCellState,
    Coord,
    MatchData,
    PlayerData,
    ShipPosition,
    ShotResult,
)

BOARD_SIZE = 10

SHIP_SIZES = [3, 4, 4, 5, 6]


class WinnerInfo(TypedDict):
    name: str
    number: int
    score: int


class Match:
    match_data: MatchData

    board_size: int = BOARD_SIZE

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

    def add_shot(self, player_receiving_shot: int, coord: Coord) -> ShotResult:
        """
        Add a shot and return the result.

        Args:
            player_shot (int): The player that made the shot (0 or 1).
            coord (Coord): The coordinates of the shot.

        Returns:
            ShotResult: The result of the shot (HIT, MISS, or SUNK)

        Raises:
            ValueError: If the shot has already been made.
            ValueError: If the shot is out of bounds.
        """
        target_player_data = (
            self.match_data["player_1"]
            if player_receiving_shot == 0
            else self.match_data["player_2"]
        )

        # Check if shot has already been made
        if coord in target_player_data["shots_received"]:
            raise ValueError("Shot has already been made")

        # Check if shot is within bounds
        if (
            coord["x"] < 0
            or coord["x"] >= BOARD_SIZE
            or coord["y"] < 0
            or coord["y"] >= BOARD_SIZE
        ):
            raise ValueError("Shot is out of bounds")

        # Add shot to player data
        target_player_data["shots_received"].append(coord)

        # Check if shot hit a ship
        for ship in target_player_data["fleet"]:
            ship_coords = self._get_ship_coords(ship)

            if coord in ship_coords:
                # Check if all ship coords have been hit
                if all(c in target_player_data["shots_received"] for c in ship_coords):
                    return ShotResult.SUNK
                return ShotResult.HIT

        return ShotResult.MISS

    def shot_already_made(self, coord: Coord, player_shot: int) -> bool:
        target_player_data = (
            self.match_data["player_1"]
            if player_shot == 0
            else self.match_data["player_2"]
        )
        return coord in target_player_data["shots_received"]

    def add_ship(self, player: int, ship: ShipPosition):
        """
        Add a ship to the match.

        Args:
            player (int): The player that added the ship (0 or 1).
            ship (ShipPosition): The ship to add.

        Raises:
            ValueError: If the ship is out of bounds.
            ValueError: If the ship overlaps with another ship.
        """
        player_data = (
            self.match_data["player_1"] if player == 0 else self.match_data["player_2"]
        )

        # Check if ship is within bounds
        if ship["orientation"] == "horizontal":
            if ship["x"] + ship["size"] > BOARD_SIZE:
                raise ValueError("Ship is out of bounds")
        else:
            if ship["y"] + ship["size"] > BOARD_SIZE:
                raise ValueError("Ship is out of bounds")

        # Get all cells that the new ship would occupy
        new_ship_cells = self._get_ship_coords(ship)

        # Check that ship does not overlap with other ships
        for other_ship in player_data["fleet"]:
            other_ship_cells = self._get_ship_coords(other_ship)
            # Si hay alguna celda en común, hay overlap
            if any(cell in other_ship_cells for cell in new_ship_cells):
                raise ValueError("Ship overlaps with other ship")

        player_data["fleet"].append(ship)

    def get_board(self, player: int) -> list[list[MatchCellState]]:
        """
        Get the board for a player.

        Args:
            player (int): The player to get the board for (0 or 1).

        Returns:
            list[list[MatchCellState]]: The board for the player.
        """
        board = [
            [MatchCellState.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        player_data = (
            self.match_data["player_1"] if player == 0 else self.match_data["player_2"]
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
        """
        Get the match data as a JSON string.
        """
        return json.dumps(self.match_data, indent=2)

    def save(self):
        """
        Save the match data to a file.
        """
        match_data_json = self.get_json()
        FileStorage.write_file("match.json", match_data_json)

    @staticmethod
    def from_json(data: str) -> "Match":
        """
        Create a match from a JSON string.
        """
        match_data = json.loads(data)
        match = Match()
        match.match_data.update(match_data)
        return match

    def get_sunken_ships(self, player: int) -> list[list[Coord]]:
        """
        Get a list of coordinates for each sunken ship.
        """
        player_data = (
            self.match_data["player_1"] if player == 0 else self.match_data["player_2"]
        )

        sunken_ships: list[list[Coord]] = []

        for ship in player_data["fleet"]:
            ship_coords = self._get_ship_coords(ship)

            if all(c in player_data["shots_received"] for c in ship_coords):
                sunken_ships.append(ship_coords)

        return sunken_ships

    def get_winner(self) -> WinnerInfo | None:
        """
        Check if there's a winner.

        Returns:
            dict | None: A dictionary with winner info (name, number, score) if there's a winner, None otherwise.
        """
        # Check if all player 1's ships are sunk
        player_0_ships = self.get_sunken_ships(0)
        if len(player_0_ships) == len(self.match_data["player_1"]["fleet"]):
            return {
                "name": self.match_data["player_2"]["name"],
                "number": 1,
                "score": len(self.match_data["player_1"]["shots_received"]),
            }

        # Check if all player 2's ships are sunk
        player_1_ships = self.get_sunken_ships(1)
        if len(player_1_ships) == len(self.match_data["player_2"]["fleet"]):
            return {
                "name": self.match_data["player_1"]["name"],
                "number": 0,
                "score": len(self.match_data["player_2"]["shots_received"]),
            }

        return None  # No winner yet

    def _get_ship_coords(self, ship: ShipPosition) -> list[Coord]:
        """
        Get a list of coordinates for a ship.

        Args:
            ship (ShipPosition): The ship position and orientation.

        Returns:
            list[Coord]: A list of coordinates that the ship occupies.
        """
        if ship["orientation"] == "horizontal":
            return [{"x": ship["x"] + i, "y": ship["y"]} for i in range(ship["size"])]
        else:
            return [{"x": ship["x"], "y": ship["y"] + i} for i in range(ship["size"])]
