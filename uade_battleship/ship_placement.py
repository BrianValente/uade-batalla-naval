import pygame
import sys
from typing import Any, Callable, Optional, Protocol, cast
from moviepy.editor import VideoFileClip
import numpy as np
import time

from .ui.Button import Button
from .ui.options_menu import OptionsMenu
from .ui.TextInput import TextInput
from .utils.colors import Color
from .match import Match, ShipPosition, SHIP_SIZES

CELLSIZE = 40
GRID_SIZE = 10


class VideoClipProtocol(Protocol):
    duration: float
    get_frame: Callable[[float], Any]


class DraggableShip:
    def __init__(self, ship_position: ShipPosition):
        self.ship_position = ship_position
        self.dragging = False
        self.initial_mouse_x = 0
        self.initial_mouse_y = 0
        self.current_mouse_x = 0
        self.current_mouse_y = 0
        self.last_click_time = 0
        self.double_click_threshold = 300
        self.last_valid_position = ship_position.copy()
        self.ship_image = pygame.image.load(
            f"assets/ships/{ship_position['size']}x1.png"
        )

    def reset_to_last_position(self):
        """Go back to the last valid position"""
        self.ship_position = self.last_valid_position.copy()

    def start_drag(self):
        """Save the current position before starting to drag"""
        self.last_valid_position = self.ship_position.copy()
        self.dragging = True

    def draw(self, screen: pygame.Surface, grid_pos: tuple[int, int]):
        if self.ship_position["orientation"] == "horizontal":
            width = self.ship_position["size"] * CELLSIZE
            height = CELLSIZE
            # Scale the image horizontally
            rotated = pygame.transform.rotate(self.ship_image, 90)
            scaled_image = pygame.transform.scale(rotated, (width, height))
        else:
            width = CELLSIZE
            height = self.ship_position["size"] * CELLSIZE
            # Rotate 90 degrees and scale for vertical orientation
            scaled_image = pygame.transform.scale(self.ship_image, (width, height))

        position = self.get_position(grid_pos)
        screen.blit(scaled_image, position)

    def get_position(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        position = (
            grid_pos[0] + self.ship_position["x"] * CELLSIZE,
            grid_pos[1] + self.ship_position["y"] * CELLSIZE,
        )
        mouse_offset = (
            self.current_mouse_x - self.initial_mouse_x,
            self.current_mouse_y - self.initial_mouse_y,
        )
        position_with_offset = (
            position[0] + mouse_offset[0],
            position[1] + mouse_offset[1],
        )
        return position_with_offset

    def handle_click(
        self, click_pos: tuple[int, int], grid_pos: tuple[int, int]
    ) -> bool:
        x, y = click_pos
        ship_rect = self.get_rect(grid_pos)
        if ship_rect.collidepoint(x, y):
            return True
        return False

    def get_rect(self, grid_pos: tuple[int, int]) -> pygame.Rect:
        if self.ship_position["orientation"] == "horizontal":
            width = self.ship_position["size"] * CELLSIZE
            height = CELLSIZE
        else:
            width = CELLSIZE
            height = self.ship_position["size"] * CELLSIZE
        return pygame.Rect(
            grid_pos[0] + self.ship_position["x"] * CELLSIZE,
            grid_pos[1] + self.ship_position["y"] * CELLSIZE,
            width,
            height,
        )

    def rotate(self):
        self.ship_position["orientation"] = (
            "vertical"
            if self.ship_position["orientation"] == "horizontal"
            else "horizontal"
        )

        # Adjust position if it goes out of the grid
        if self.ship_position["orientation"] == "horizontal":
            # If rotating to horizontal goes out on the right
            if self.ship_position["x"] + self.ship_position["size"] > GRID_SIZE:
                self.ship_position["x"] = GRID_SIZE - self.ship_position["size"]
        else:  # vertical
            # If rotating to vertical goes out on the bottom
            if self.ship_position["y"] + self.ship_position["size"] > GRID_SIZE:
                self.ship_position["y"] = GRID_SIZE - self.ship_position["size"]


def ship_placement(match: Match) -> bool:
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Initialize background video
    video_clip = cast(VideoClipProtocol, VideoFileClip("assets/background.mp4"))
    start_time = time.time()

    # Calculate grid position
    screen_width, screen_height = screen.get_size()
    grid_width = GRID_SIZE * CELLSIZE
    grid_height = GRID_SIZE * CELLSIZE
    grid_x = (screen_width - grid_width) // 2
    grid_y = (screen_height - grid_height) // 2

    font = pygame.font.Font(None, 36)

    # Create text input for player name
    player_name_input = TextInput(
        pos=(screen_width // 2, grid_y - 50),  # 50px above the grid
        font=font,
        text="Player",
        base_color=Color.WHITE,
        selected_color=Color.GREEN,
        regex=r"^[a-zA-Z0-9]{1,10}$",
    )

    # Create continue button
    continue_button = Button(
        image=None,
        pos=(
            screen_width // 2,
            grid_y + grid_height + 50,
        ),  # Move the button 50px below the grid
        text_input="¡COMENZAR!",
        font=font,
        base_color=(0, 255, 0),
        hovering_color=(0, 200, 0),
    )

    # Create draggable ships with random positions
    ships: list[DraggableShip] = []

    for i, size in enumerate(SHIP_SIZES):
        try:
            ship_position: ShipPosition = {
                "x": 0,
                "y": i,
                "size": size,
                "orientation": "horizontal",
            }
            ship = DraggableShip(ship_position)
            ships.append(ship)
        except ValueError:
            continue

    selected_ship: Optional[DraggableShip] = None

    options_menu = OptionsMenu()

    while True:
        current_time = time.time()

        # Play background video
        video_time = current_time - start_time
        if video_time >= video_clip.duration:
            start_time = time.time()

        frame = video_clip.get_frame(video_time % video_clip.duration)
        frame_surface = pygame.surfarray.make_surface(np.array(frame))  # type: ignore
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.scale(
            frame_surface, (screen_width, screen_height)
        )
        screen.blit(frame_surface, (0, 0))

        # Draw grid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(
                    screen,
                    Color.WHITE,
                    (
                        grid_x + col * CELLSIZE,
                        grid_y + row * CELLSIZE,
                        CELLSIZE,
                        CELLSIZE,
                    ),
                    1,
                )

        # Check if all ships are placed in a valid way
        # There should be no overlap between ships.
        player_name_not_empty = player_name_input.get_text() != ""
        all_valid = player_name_not_empty
        for i, ship in enumerate(ships):
            # Get all coordinates occupied by the first ship
            ship_coords: set[tuple[int, int]] = set()
            if ship.ship_position["orientation"] == "horizontal":
                for x in range(
                    ship.ship_position["x"],
                    ship.ship_position["x"] + ship.ship_position["size"],
                ):
                    ship_coords.add((x, ship.ship_position["y"]))
            else:  # vertical
                for y in range(
                    ship.ship_position["y"],
                    ship.ship_position["y"] + ship.ship_position["size"],
                ):
                    ship_coords.add((ship.ship_position["x"], y))

            for j, other_ship in enumerate(ships):
                # Skip if it's the same ship
                if i == j:
                    continue

                # Get all coordinates occupied by the other ship
                other_ship_coords: set[tuple[int, int]] = set()
                if other_ship.ship_position["orientation"] == "horizontal":
                    for x in range(
                        other_ship.ship_position["x"],
                        other_ship.ship_position["x"]
                        + other_ship.ship_position["size"],
                    ):
                        other_ship_coords.add((x, other_ship.ship_position["y"]))
                else:  # vertical
                    for y in range(
                        other_ship.ship_position["y"],
                        other_ship.ship_position["y"]
                        + other_ship.ship_position["size"],
                    ):
                        other_ship_coords.add((other_ship.ship_position["x"], y))

                # If there is an intersection between the sets, there is overlap
                if ship_coords & other_ship_coords:
                    all_valid = False
                    break

        if all_valid:
            mouse_pos = pygame.mouse.get_pos()
            continue_button.changeColor(mouse_pos)
            continue_button.update(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if all_valid and continue_button.checkForInput(event.pos):
                        # Update player name before adding ships
                        match.match_data["player_1"][
                            "name"
                        ] = player_name_input.get_text()
                        # Add all ships to the match
                        for ship in ships:
                            match.add_ship(0, ship.ship_position)
                        return True

                    current_time = pygame.time.get_ticks()

                    # Reverse order since the last ships have the highest z-index
                    for ship in reversed(ships):
                        if ship.handle_click(event.pos, (grid_x, grid_y)):
                            if (
                                current_time - ship.last_click_time
                                < ship.double_click_threshold
                            ):
                                ship.rotate()
                            else:
                                selected_ship = ship
                                ship.start_drag()
                                screen_pos_x, mouse_y = event.pos
                                ship.initial_mouse_x = screen_pos_x
                                ship.initial_mouse_y = mouse_y
                                ship.current_mouse_x = screen_pos_x
                                ship.current_mouse_y = mouse_y
                            ship.last_click_time = current_time
                            break

            # Add keyboard event here
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and all_valid:
                    # Add all ships to the match
                    for ship in ships:
                        match.add_ship(0, ship.ship_position)
                    return True

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_ship:
                    try:
                        # Calculate mouse position relative to the grid
                        screen_pos_x, screen_pos_y = selected_ship.get_position(
                            (grid_x, grid_y)
                        )
                        grid_pos_x = round((screen_pos_x - grid_x) / CELLSIZE)
                        grid_pos_y = round((screen_pos_y - grid_y) / CELLSIZE)

                        # Ensure the ship doesn't go out of the grid
                        if selected_ship.ship_position["orientation"] == "horizontal":
                            max_x = GRID_SIZE - selected_ship.ship_position["size"]
                            grid_pos_x = max(0, min(grid_pos_x, max_x))
                            max_y = GRID_SIZE - 1
                            grid_pos_y = max(0, min(grid_pos_y, max_y))
                        else:
                            max_x = GRID_SIZE - 1
                            grid_pos_x = max(0, min(grid_pos_x, max_x))
                            max_y = GRID_SIZE - selected_ship.ship_position["size"]
                            grid_pos_y = max(0, min(grid_pos_y, max_y))

                        new_ship_position: ShipPosition = {
                            "x": grid_pos_x,
                            "y": grid_pos_y,
                            "size": selected_ship.ship_position["size"],
                            "orientation": selected_ship.ship_position["orientation"],
                        }

                        # Try to move the ship to the new position
                        selected_ship.ship_position = new_ship_position
                        selected_ship.last_valid_position = new_ship_position.copy()
                    except:
                        pass
                    finally:
                        # Reset the drag
                        selected_ship.dragging = False
                        selected_ship.initial_mouse_x = 0
                        selected_ship.initial_mouse_y = 0
                        selected_ship.current_mouse_x = 0
                        selected_ship.current_mouse_y = 0
                        selected_ship = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_ship and selected_ship.dragging:
                    screen_pos_x, mouse_y = event.pos
                    selected_ship.current_mouse_x = screen_pos_x
                    selected_ship.current_mouse_y = mouse_y

            options_menu.handle_keyboard(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_menu.handle_click(event.pos):
                    return False

            # Add text input handling
            player_name_input.handle_event(event)

        # Draw text input
        player_name_input.draw(screen)

        # Draw ships
        for ship in ships:
            ship.draw(screen, (grid_x, grid_y))

        options_menu.draw(screen)

        pygame.display.update()
        clock.tick(60)
