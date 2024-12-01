import pygame, sys
import math
import random
from typing import Literal

from .utils import Settings, SettingsKey, Color
from .ui import Button
from .match.match_data import ShipPosition
from .board import board
from .instructions import instructions
from .match import Match, SHIP_SIZES
from .ship_placement import ship_placement
from .scoreboard_screen import scoreboard_screen
from .settings import settings_screen

pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/menu_background.jpg")


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


def play():
    cpu_ships: list[ShipPosition] = []

    def generate_random_ship_position(
        size: int, cpu_ships: list[ShipPosition]
    ) -> ShipPosition:
        # List to save all valid positions
        valid_positions: list[ShipPosition] = []

        # Check each cell of the board
        for y in range(10):
            for x in range(10):
                # Try horizontal orientation
                if x + size <= 10:  # If the ship fits horizontally
                    ship_horizontal: ShipPosition = {
                        "x": x,
                        "y": y,
                        "size": size,
                        "orientation": "horizontal",
                    }

                    # Get horizontal ship coordinates
                    horizontal_coords = set((x + dx, y) for dx in range(size))

                    # Assume it's valid until proven otherwise
                    valid_horizontal = True

                    # Check overlap with each existing ship
                    for existing_ship in cpu_ships:
                        existing_coords: set[tuple[int, int]] = set()
                        if existing_ship["orientation"] == "horizontal":
                            existing_coords = set(
                                (existing_ship["x"] + dx, existing_ship["y"])
                                for dx in range(existing_ship["size"])
                            )
                        else:
                            existing_coords = set(
                                (existing_ship["x"], existing_ship["y"] + dy)
                                for dy in range(existing_ship["size"])
                            )

                        if horizontal_coords & existing_coords:
                            valid_horizontal = False
                            break

                    if valid_horizontal:
                        valid_positions.append(ship_horizontal)

                # Try vertical orientation
                if y + size <= 10:  # If the ship fits vertically
                    ship_vertical: ShipPosition = {
                        "x": x,
                        "y": y,
                        "size": size,
                        "orientation": "vertical",
                    }

                    # Get vertical ship coordinates
                    vertical_coords = set((x, y + dy) for dy in range(size))

                    # Assume it's valid until proven otherwise
                    valid_vertical = True

                    # Check overlap with each existing ship
                    for existing_ship in cpu_ships:
                        existing_coords = set()
                        if existing_ship["orientation"] == "horizontal":
                            existing_coords = set(
                                (existing_ship["x"] + dx, existing_ship["y"])
                                for dx in range(existing_ship["size"])
                            )
                        else:
                            existing_coords = set(
                                (existing_ship["x"], existing_ship["y"] + dy)
                                for dy in range(existing_ship["size"])
                            )

                        if vertical_coords & existing_coords:
                            valid_vertical = False
                            break

                    if valid_vertical:
                        valid_positions.append(ship_vertical)

        # If there are no valid positions, raise an error
        if not valid_positions:
            raise ValueError("No valid positions found for the ship")

        # Return a random valid position
        return random.choice(valid_positions)

    match = Match("Player", "CPU")

    # First go to the ship placement screen
    if not ship_placement(match):
        return

    for size in SHIP_SIZES:
        ship = generate_random_ship_position(size, cpu_ships)
        cpu_ships.append(ship)
        match.add_ship(1, ship)

    match.save()

    # Then go to the game screen
    board(match)


def continue_game():
    match = Match.get_last_save()
    if not match:
        return
    board(match)


def main_menu():
    clock = pygame.time.Clock()
    animation_time = 0  # Variable to control the animation time
    selected_option = 0  # Index of the selected option
    mouse_used = False  # Flag to detect if the mouse was used

    last_save = Match.get_last_save()

    # Define the list of buttons
    # Show the continue game button if there is a saved game
    initial_buttons = [
        Button(
            id="start_game",
            image=None,
            pos=(0, 0),
            text_input="Comenzar partida",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
        ),
        Button(
            id="instructions",
            image=None,
            pos=(0, 0),
            text_input="Instrucciones de juego",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
        ),
        Button(
            id="settings",
            image=None,
            pos=(0, 0),
            text_input="Configuraciones",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
        ),
        Button(
            id="scores",
            image=None,
            pos=(0, 0),
            text_input="Scores",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
        ),
        Button(
            id="exit",
            image=None,
            pos=(0, 0),
            text_input="Salir",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
        ),
    ]

    last_save_button = Button(
        id="continue_game",
        image=None,
        pos=(0, 0),
        text_input="Continuar partida",
        font=get_font(30),
        base_color=Color.DARK_BLUE,
        hovering_color=Color.LIGHT_BLUE,
    )

    while True:
        screen = pygame.display.get_surface()

        buttons = initial_buttons.copy()
        if last_save:
            buttons.insert(0, last_save_button)

        # Draw the background image and apply the translucent black overlay
        background_scaled = pygame.transform.scale(BG, (1280, 720))
        screen.blit(background_scaled, (0, 0))
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill(Color.TRANSLUCENT_BLACK)
        screen.blit(overlay, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Animation control: use math.sin() to oscillate the size
        animation_time += clock.get_time() / 500  # Divide to control the speed
        scale_factor = 1 + 0.1 * math.sin(
            animation_time
        )  # The scale factor oscillates between 1 and 1.1
        animated_font_size = int(60 * scale_factor)  # Adjust the font size
        MENU_TEXT = get_font(animated_font_size).render("MENU", True, Color.WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        screen.blit(MENU_TEXT, MENU_RECT)

        # Update button colors and position
        for i, button in enumerate(buttons):
            button.changeColor(MENU_MOUSE_POS)
            button.update(
                screen, position=(640, 220 + (i + (0 if last_save else 1)) * 80)
            )

        # Move between options with keyboard and mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(buttons)
                    mouse_used = False  # Reset the mouse usage
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(buttons)
                    mouse_used = False  # Reset the mouse usage
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_button = buttons[selected_option]
                    if selected_button.id == "start_game":
                        play()
                        last_save = Match.get_last_save()
                    elif selected_button.id == "continue_game":
                        continue_game()
                        last_save = Match.get_last_save()
                    elif selected_button.id == "instructions":
                        instructions()
                    elif selected_button.id == "settings":
                        settings_screen()
                    elif selected_button.id == "scores":
                        scoreboard_screen()
                    elif selected_button.id == "exit":
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mouse_used = True  # If the mouse moves, use it to highlight
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.checkForInput(MENU_MOUSE_POS):
                        selected_option = i
                        selected_button = buttons[selected_option]
                        if selected_button.id == "start_game":
                            play()
                            last_save = Match.get_last_save()
                        elif selected_button.id == "continue_game":
                            continue_game()
                            last_save = Match.get_last_save()
                        elif selected_button.id == "instructions":
                            instructions()
                        elif selected_button.id == "settings":
                            settings_screen()
                        elif selected_button.id == "scores":
                            scoreboard_screen()
                        elif selected_button.id == "exit":
                            pygame.quit()
                            sys.exit()

        # Highlight the selected option with the keyboard
        if not mouse_used:
            for i, button in enumerate(buttons):
                if i == selected_option:
                    button.text = button.font.render(
                        button.text_input, True, button.hovering_color
                    )
                else:
                    button.text = button.font.render(
                        button.text_input, True, button.base_color
                    )
                button.update(screen)

        pygame.display.update()
        clock.tick(60)  # Keep 60 FPS


# Load background music
pygame.mixer.init()
pygame.mixer.music.load("assets/background_music_menu.mp3")

# Play background music
pygame.mixer.music.play(-1)  # Play in loop
pygame.mixer.music.set_volume(Settings.get(SettingsKey.VOLUME) * 0.5)  # 50% volume
