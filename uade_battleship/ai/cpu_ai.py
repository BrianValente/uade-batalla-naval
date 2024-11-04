from typing import Optional
from ..match import Match, ShotResult, Coord, MatchCellState


class CpuAi:
    def __init__(self, match: Match) -> None:
        self.match = match

    def play_turn(self) -> ShotResult:
        """
        Juega el turno de la CPU y retorna el resultado del disparo.
        """
        shot = self._get_next_shot()
        return self.match.add_shot(0, shot)

    def _get_next_shot(self) -> Coord:
        # Buscamos un barco golpeado pero no hundido
        damaged_ship = self._find_damaged_ship()
        if damaged_ship:
            shot = self._get_smart_shot(damaged_ship)
            if shot:
                return shot

        # Si no hay barcos dañados o no podemos disparar alrededor, tiro random
        return self._get_random_shot()

    def _get_smart_shot(self, hit_coord: Coord) -> Optional[Coord]:
        """Busca patrones y dispara en esa dirección"""
        board = self.match.get_board(0)
        adjacents: list[tuple[Coord, str]] = [
            ({"x": hit_coord["x"], "y": hit_coord["y"] - 1}, "vertical"),  # arriba
            ({"x": hit_coord["x"], "y": hit_coord["y"] + 1}, "vertical"),  # abajo
            ({"x": hit_coord["x"] - 1, "y": hit_coord["y"]}, "horizontal"),  # izquierda
            ({"x": hit_coord["x"] + 1, "y": hit_coord["y"]}, "horizontal"),  # derecha
        ]

        # Primero buscamos si hay hits adyacentes para seguir esa dirección
        for coord, direction in adjacents:
            if (
                0 <= coord["x"] < self.match.board_size
                and 0 <= coord["y"] < self.match.board_size
                and board[coord["y"]][coord["x"]] == MatchCellState.HIT
            ):

                # Si encontramos un hit, seguimos en esa dirección
                next_shot = self._get_next_in_direction(hit_coord, direction)
                if next_shot:
                    return next_shot

        # Si no hay hits adyacentes, probamos cualquier casilla adyacente válida
        valid_shots = [
            coord
            for coord, _ in adjacents
            if self._is_valid_shot(coord["x"], coord["y"])
        ]

        return valid_shots[0] if valid_shots else None

    def _get_next_in_direction(
        self, hit_coord: Coord, direction: str
    ) -> Optional[Coord]:
        """Obtiene la siguiente coordenada en la dirección del patrón"""

        def get_next_coord(x: int, y: int) -> Optional[Coord]:
            """Sigue buscando en la dirección hasta encontrar una posición válida"""
            while 0 <= x < self.match.board_size and 0 <= y < self.match.board_size:
                cell_state = self.match.get_board(0)[y][x]

                # Si encontramos una celda válida, la retornamos
                if cell_state in [MatchCellState.EMPTY, MatchCellState.SHIP]:
                    return {"x": x, "y": y}

                # Si ya fue atacada y fallamos, paramos de buscar en esta dirección
                elif cell_state in [MatchCellState.MISS]:
                    return None

                # Si ya fue atacada y acertamos, seguimos en la misma dirección
                if direction == "horizontal":
                    x = x + 1 if x > hit_coord["x"] else x - 1
                else:
                    y = y + 1 if y > hit_coord["y"] else y - 1

            return None  # Fuera del tablero

        if direction == "horizontal":
            # Intentamos a la derecha primero
            right = get_next_coord(hit_coord["x"] + 1, hit_coord["y"])
            if right:
                return right
            # Si no, a la izquierda
            left = get_next_coord(hit_coord["x"] - 1, hit_coord["y"])
            if left:
                return left
        else:  # vertical
            # Intentamos abajo primero
            down = get_next_coord(hit_coord["x"], hit_coord["y"] + 1)
            if down:
                return down
            # Si no, arriba
            up = get_next_coord(hit_coord["x"], hit_coord["y"] - 1)
            if up:
                return up
        return None

    def _find_damaged_ship(self) -> Optional[Coord]:
        """Busca un barco que esté golpeado pero no hundido"""
        board = self.match.get_board(0)  # Tablero del player 0
        sunken_ships = self.match.get_sunken_ships(0)  # Barcos hundidos
        sunken_coords = [coord for ship in sunken_ships for coord in ship]

        # Buscamos un HIT que no sea parte de un barco hundido
        for y in range(self.match.board_size):
            for x in range(self.match.board_size):
                if board[y][x] == MatchCellState.HIT and not any(
                    coord["x"] == x and coord["y"] == y for coord in sunken_coords
                ):
                    return {"x": x, "y": y}
        return None

    def _get_random_shot(self) -> Coord:
        """Obtiene un disparo aleatorio en una casilla válida"""
        import random

        while True:
            x = random.randint(0, self.match.board_size - 1)
            y = random.randint(0, self.match.board_size - 1)
            if self._is_valid_shot(x, y):
                return {"x": x, "y": y}

    def _is_valid_shot(self, x: int, y: int) -> bool:
        """Verifica si la coordenada es válida para disparar"""
        return (
            0 <= x < self.match.board_size
            and 0 <= y < self.match.board_size
            and not self.match.shot_already_made({"x": x, "y": y}, 0)
        )
