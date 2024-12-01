from typing import Optional
from ..match import Match, ShotResult, Coord, MatchCellState


class CpuAi:
    def __init__(self, match: Match) -> None:
        self.match = match

    def play_turn(self) -> ShotResult:
        """
        Plays the CPU's turn and returns the shot result.
        """
        shot = self._get_next_shot()
        return self.match.add_shot(0, shot)

    def _get_next_shot(self) -> Coord:
        # Look for a damaged ship
        damaged_ship = self._find_damaged_ship()
        if damaged_ship:
            shot = self._get_smart_shot(damaged_ship)
            if shot:
                return shot

        # If there are no damaged ships or we can't shoot around, shoot random
        return self._get_random_shot()

    def _get_smart_shot(self, hit_coord: Coord) -> Optional[Coord]:
        """Looks for patterns and shoots in that direction"""
        board = self.match.get_board(0)
        adjacents: list[tuple[Coord, str]] = [
            ({"x": hit_coord["x"], "y": hit_coord["y"] - 1}, "vertical"),  # up
            ({"x": hit_coord["x"], "y": hit_coord["y"] + 1}, "vertical"),  # down
            ({"x": hit_coord["x"] - 1, "y": hit_coord["y"]}, "horizontal"),  # left
            ({"x": hit_coord["x"] + 1, "y": hit_coord["y"]}, "horizontal"),  # right
        ]

        # First, we look for adjacent hits to continue that direction
        for coord, direction in adjacents:
            if (
                0 <= coord["x"] < self.match.board_size
                and 0 <= coord["y"] < self.match.board_size
                and board[coord["y"]][coord["x"]] == MatchCellState.HIT
            ):

                # If we find a hit, we continue in that direction
                next_shot = self._get_next_in_direction(hit_coord, direction)
                if next_shot:
                    return next_shot

        # If there are no adjacent hits, we try any valid adjacent cell
        valid_shots = [
            coord
            for coord, _ in adjacents
            if self._is_valid_shot(coord["x"], coord["y"])
        ]

        return valid_shots[0] if valid_shots else None

    def _get_next_in_direction(
        self, hit_coord: Coord, direction: str
    ) -> Optional[Coord]:
        """Gets the next coordinate in the pattern direction"""

        def get_next_coord(x: int, y: int) -> Optional[Coord]:
            """Searches for a valid position in the direction"""
            while 0 <= x < self.match.board_size and 0 <= y < self.match.board_size:
                cell_state = self.match.get_board(0)[y][x]

                # If we find a valid cell, return it
                if cell_state in [MatchCellState.EMPTY, MatchCellState.SHIP]:
                    return {"x": x, "y": y}

                # If it was attacked and missed, stop searching in this direction
                elif cell_state in [MatchCellState.MISS]:
                    return None

                # If it was attacked and hit, continue in the same direction
                if direction == "horizontal":
                    x = x + 1 if x > hit_coord["x"] else x - 1
                else:
                    y = y + 1 if y > hit_coord["y"] else y - 1

            return None  # Out of the board

        if direction == "horizontal":
            # Try right first
            right = get_next_coord(hit_coord["x"] + 1, hit_coord["y"])
            if right:
                return right
            # If not, try left
            left = get_next_coord(hit_coord["x"] - 1, hit_coord["y"])
            if left:
                return left
        else:  # vertical
            # Try down first
            down = get_next_coord(hit_coord["x"], hit_coord["y"] + 1)
            if down:
                return down
            # If not, try up
            up = get_next_coord(hit_coord["x"], hit_coord["y"] - 1)
            if up:
                return up
        return None

    def _find_damaged_ship(self) -> Optional[Coord]:
        """Looks for a damaged ship"""
        board = self.match.get_board(0)  # Player 0's board
        sunken_ships = self.match.get_sunken_ships(0)  # Sunken ships
        sunken_coords = [coord for ship in sunken_ships for coord in ship]

        # Look for a HIT that is not part of a sunken ship
        for y in range(self.match.board_size):
            for x in range(self.match.board_size):
                if board[y][x] == MatchCellState.HIT and not any(
                    coord["x"] == x and coord["y"] == y for coord in sunken_coords
                ):
                    return {"x": x, "y": y}
        return None

    def _get_random_shot(self) -> Coord:
        """Gets a random shot in a valid cell"""
        import random

        while True:
            x = random.randint(0, self.match.board_size - 1)
            y = random.randint(0, self.match.board_size - 1)
            if self._is_valid_shot(x, y):
                return {"x": x, "y": y}

    def _is_valid_shot(self, x: int, y: int) -> bool:
        """Checks if the coordinate is valid to shoot"""
        return (
            0 <= x < self.match.board_size
            and 0 <= y < self.match.board_size
            and not self.match.shot_already_made({"x": x, "y": y}, 0)
        )
