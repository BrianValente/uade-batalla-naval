from enum import IntEnum
from typing import Literal, TypedDict


class MatchCellState(IntEnum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    MISS = 3


class Coord(TypedDict):
    x: int
    y: int


class ShipPosition(TypedDict):
    x: int
    y: int
    size: int
    orientation: Literal["horizontal", "vertical"]


class PlayerData(TypedDict):
    name: str
    fleet: list[ShipPosition]
    shots_received: list[Coord]


class MatchData(TypedDict):
    type: Literal["singleplayer", "multiplayer_local"]
    player_1: PlayerData
    player_2: PlayerData
