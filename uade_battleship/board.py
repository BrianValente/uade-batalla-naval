import pygame
import sys
from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np
import time
from typing import Any, Callable, Protocol, cast

from uade_battleship.game_board.game_board import GameBoard
from uade_battleship.utils import Settings, SettingsKey

from .match import Match, ShotResult
from .ai.cpu_ai import CpuAi
from .ui.options_menu import OptionsMenu
from .scoreboard.Scoreboard import Scoreboard


class VideoClipProtocol(Protocol):
    duration: float
    get_frame: Callable[[float], Any]


# Initial Configuration
ROWS = 10
COLS = 10
CELLSIZE = 40
# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Volume Variables
bar_width = 150
bar_height = 20
bar_x = 80  # x coordinate of the bar
bar_y = 285  # y coordinate below the buttons

menu_button_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)


def draw_menu_button(window: pygame.Surface, gear_img: pygame.Surface):
    global menu_button_rect

    # configuration icon area
    menu_button_rect = gear_img.get_rect(topleft=(20, 20))
    window.blit(gear_img, menu_button_rect.topleft)


# Show the options "Return to menu?" with "Yes" and "No"
def show_menu_options(window: pygame.Surface, font: pygame.font.Font):
    question_text = font.render("¿Volver al menú?", True, (255, 255, 255))
    yes_text = font.render("Sí", True, (0, 150, 0))
    no_text = font.render("No", True, (150, 0, 0))

    question_pos = (40, 100)
    yes_button_rect = pygame.Rect(40, 160, 50, 40)
    no_button_rect = pygame.Rect(120, 160, 50, 40)

    pygame.draw.rect(window, (GREEN), yes_button_rect)
    pygame.draw.rect(window, (RED), no_button_rect)

    window.blit(question_text, question_pos)
    window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
    window.blit(no_text, (no_button_rect.x + 10, no_button_rect.y + 5))

    return yes_button_rect, no_button_rect


def show_volume_text(window: pygame.Surface, font: pygame.font.Font):
    volume_text = font.render("Volumen", True, (255, 255, 255))
    window.blit(volume_text, (40, 250))

    volume_img = pygame.image.load("assets/volume.png")
    volume_img = pygame.transform.scale(volume_img, (50, 30))
    window.blit(volume_img, (35, 280))

    return volume_text


# Rectangle representing the volume bar
volume_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)


# Function to draw the volume bar
def draw_volume_bar(window: pygame.Surface, volume: float):
    # Background of the bar (gray)
    pygame.draw.rect(window, GRAY, volume_rect)

    # Part of the bar that represents the volume (blue)
    filled_rect = pygame.Rect(bar_x, bar_y, int(volume * bar_width), bar_height)
    pygame.draw.rect(window, BLUE, filled_rect)


# Variable to know if the mouse is pressing the bar
adjusting_volume = False


# Function to adjust the volume when clicking and dragging
def adjust_volume(mouse_x: int, mouse_y: int):
    global volume, adjusting_volume
    mouse_buttons = pygame.mouse.get_pressed()

    # Check if the mouse is within the volume bar limits
    if mouse_buttons[0]:  # If the left mouse button is pressed
        if volume_rect.collidepoint(mouse_x, mouse_y) or adjusting_volume:
            adjusting_volume = True
            volume = (mouse_x - bar_x) / bar_width
            volume = max(0, min(volume, 1))  # Limit between 0 and 1
            pygame.mixer.music.set_volume(volume)  # Adjust the music volume
            Settings.set(SettingsKey.VOLUME, volume)
    else:
        adjusting_volume = False  # The user released the mouse


# Function to create the grid
def create_game_grid(rows: int, cols: int, cellsize: int, pos: tuple[int, int]):
    start_x = pos[0]
    start_y = pos[1]
    coor_grid: list[list[tuple[int, int]]] = []
    for _ in range(rows):
        row_x: list[tuple[int, int]] = []
        for _ in range(cols):
            row_x.append((start_x, start_y))
            start_x += cellsize
        coor_grid.append(row_x)
        start_x = pos[0]
        start_y += cellsize
    return coor_grid


# Function to initialize the game logic
def update_game_logic(rows: int, cols: int):
    gamelogic: list[list[str]] = []
    for _ in range(rows):
        row_x: list[str] = []
        for _ in range(cols):
            row_x.append(" ")  # Blank space for empty cells
        gamelogic.append(row_x)
    return gamelogic


# Function to print the game logic to the console
def print_game_logic(p_game_logic: list[list[str]]):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)


# Function to calculate the size and position of the grid
def grid_size(window: pygame.Surface, rows: int, cols: int, cellsize: int):
    screen_width, screen_height = window.get_size()
    grid_width = cols * cellsize
    grid_height = rows * cellsize
    start_x = (screen_width - grid_width) // 2  # Centered on X
    start_y = screen_height - grid_height - 50  # 50 pixels from the bottom
    return start_x, start_y


# Function to handle keyboard events
def handle_keyboard_event(event: pygame.event.Event, ask_return_menu: bool):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        ask_return_menu = not ask_return_menu  # Toggle the menu with "Esc"
    return ask_return_menu


def draw_stats(
    window: pygame.Surface,
    font: pygame.font.Font,
    match: Match,
):
    # Stats of the current player
    current_stats = match.get_player_stats(0)
    enemy_stats = match.get_player_stats(1)

    # Position for stats of the current player (left side)
    player_stats_x = 50
    stats_y = 300

    # Stats of the current player
    stats_texts = [
        f"Tu tablero",
        f"Barcos hundidos: {current_stats['ships_sunk']}/{len(match.match_data['player_1']['fleet'])}",
        f"Barcos dañados: {current_stats['ships_damaged']}",
    ]

    # Calculate the maximum width of the player's texts
    max_width = max(font.size(text)[0] for text in stats_texts)
    total_height = len(stats_texts) * 30  # 30 is the vertical spacing between lines

    # Configuration of the semi-transparent black background for player
    background = pygame.Surface((max_width + 20, total_height + 20))  # +20 for padding
    background.set_alpha(128)
    background.fill((0, 0, 0))

    # Draw the background for player stats
    window.blit(background, (player_stats_x - 10, stats_y - 10))

    for i, text in enumerate(stats_texts):
        text_surface = font.render(text, True, WHITE)
        window.blit(text_surface, (player_stats_x, stats_y + i * 30))

    # Stats of the enemy (right side)
    enemy_stats_x = window.get_width() - 250

    enemy_stats_texts = [
        f"Tablero enemigo",
        f"Barcos hundidos: {enemy_stats['ships_sunk']}/{len(match.match_data['player_2']['fleet'])}",
    ]

    # Calculate the maximum width of the enemy's texts
    enemy_max_width = max(font.size(text)[0] for text in enemy_stats_texts)
    enemy_total_height = len(enemy_stats_texts) * 30

    # Configuration of the semi-transparent black background for enemy
    enemy_background = pygame.Surface((enemy_max_width + 20, enemy_total_height + 20))
    enemy_background.set_alpha(128)
    enemy_background.fill((0, 0, 0))

    # Draw the background for enemy stats
    window.blit(enemy_background, (enemy_stats_x - 10, stats_y - 10))

    for i, text in enumerate(enemy_stats_texts):
        text_surface = font.render(text, True, WHITE)
        window.blit(text_surface, (enemy_stats_x, stats_y + i * 30))


def board(match: Match):
    run_game = True

    game_surface = pygame.display.get_surface()
    pygame.display.set_caption("Battleship Game")

    p_game_grid_start_pos = grid_size(game_surface, ROWS, COLS, CELLSIZE)
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)

    # Load background music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/background_music_game.mp3")

    # Play background music
    pygame.mixer.music.play(loops=-1)  # Play in loop
    pygame.mixer.music.set_volume(
        Settings.get(SettingsKey.VOLUME) * 0.5
    )  # volume at 50%

    if not pygame.mixer.get_init():
        print("Error loading background music")

    # Load the background video
    video_clip = cast(VideoClipProtocol, VideoFileClip("assets/background.mp4"))
    start_time = time.time()  # Start time of the playback

    overlay_surface = pygame.Surface(game_surface.get_size())
    overlay_surface.set_alpha(140)
    overlay_surface.fill((0, 0, 0))

    # Load menu image
    gear_img = pygame.image.load("assets/gear.png")
    gear_img = pygame.transform.scale(gear_img, (50, 50))  # Adjust size if necessary

    # Initialize the font and menu state
    font = pygame.font.SysFont(None, 36)
    ask_return_menu = False  # Controls when to show the return to menu question

    # Create a semi-transparent surface to obscure the grid
    overlay_surface = pygame.Surface(game_surface.get_size())
    overlay_surface.set_alpha(140)  # 128 is a transparency value (0-255)
    overlay_surface.fill((0, 0, 0))  # Color of the opacity, in this case black

    game_board = GameBoard(match, p_game_grid)
    cpu = CpuAi(match)  # Instantiate the CPU

    current_player = match.get_current_player_index()
    waiting_for_turn_change = False
    last_move_time = 0
    winner = None
    winner_show_start_time = 0
    cpu_thinking_start_time = 0  # To control the CPU delay
    score_saved = False  # New variable to control if we already saved the score

    options_menu = OptionsMenu()

    # Load sound effects
    hit_sound = pygame.mixer.Sound("assets/hit.mp3")
    miss_sound = pygame.mixer.Sound("assets/miss.mp3")
    sunk_sound = pygame.mixer.Sound("assets/sunk.mp3")

    # Adjust initial volume of the effects
    hit_sound.set_volume(Settings.get(SettingsKey.VOLUME))
    miss_sound.set_volume(Settings.get(SettingsKey.VOLUME))
    sunk_sound.set_volume(Settings.get(SettingsKey.VOLUME))

    while run_game:
        enemy_player = 1 - current_player
        current_time = time.time()

        # Check if there is a winner
        if winner is None:
            winner = match.get_winner()
            if winner is not None:
                winner_show_start_time = current_time
                # If the winner is the human player (number 0) and we haven't saved the score yet
                if winner["number"] == 0 and not score_saved:
                    Scoreboard.save_score(
                        {"name": winner["name"], "score": winner["score"]}
                    )
                    score_saved = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()  # Close Pygame when closing the window
                sys.exit()  # Close the program

            options_menu.handle_keyboard(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if options_menu.handle_click(mouse_pos):
                    return  # Return to the menu

                if not options_menu.ask_return_menu:
                    if (
                        not waiting_for_turn_change
                        and not winner
                        and current_player == 0
                    ):
                        shot_result = game_board.handle_click(
                            mouse_pos, player=enemy_player
                        )
                        if shot_result == ShotResult.MISS:
                            miss_sound.play()
                            waiting_for_turn_change = True
                            last_move_time = current_time
                        elif shot_result == ShotResult.HIT:
                            hit_sound.play()
                        elif shot_result == ShotResult.SUNK:
                            sunk_sound.play()

        if (
            current_player == 1 and not waiting_for_turn_change and not winner
        ):  # CPU's turn
            if cpu_thinking_start_time == 0:  # If the CPU's turn just started
                cpu_thinking_start_time = current_time
            elif current_time - cpu_thinking_start_time >= 1:  # If 1 second has passed
                shot_result = cpu.play_turn()
                if shot_result == ShotResult.MISS:
                    miss_sound.play()
                    waiting_for_turn_change = True
                    last_move_time = current_time
                elif shot_result == ShotResult.HIT:
                    hit_sound.play()
                elif shot_result == ShotResult.SUNK:
                    sunk_sound.play()
                cpu_thinking_start_time = 0  # Reset for the next turn

        # Check if 2 seconds have passed since the last move
        if waiting_for_turn_change and current_time - last_move_time >= 2:
            current_player = 1 - current_player
            waiting_for_turn_change = False

        # Play the background video
        current__video_time = time.time() - start_time
        if current__video_time >= video_clip.duration:
            start_time = time.time()

        frame = video_clip.get_frame(current_time % video_clip.duration)
        frame_surface = pygame.surfarray.make_surface(np.array(frame))  # type: ignore
        frame_surface = pygame.transform.rotate(frame_surface, 270)
        frame_surface = pygame.transform.scale(
            frame_surface, (game_surface.get_width(), game_surface.get_height())
        )

        game_surface.blit(frame_surface, (0, 0))

        # Show the configuration gear
        draw_menu_button(game_surface, gear_img)

        # Draw the current player title centered at the top
        current_player_name = (
            match.match_data["player_1"]["name"]
            if current_player == 0
            else match.match_data["player_2"]["name"]
        )
        current_player_text = font.render(
            f"Turno de {current_player_name}", True, WHITE
        )
        text_rect = current_player_text.get_rect()
        text_rect.centerx = game_surface.get_width() // 2
        text_rect.top = 10

        # Black background for the current player text
        background = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
        background.set_alpha(128)
        background.fill((0, 0, 0))
        game_surface.blit(background, (text_rect.x - 10, text_rect.y - 5))
        game_surface.blit(current_player_text, text_rect)

        game_board.draw_enemy_board(
            game_surface, enemy_player=enemy_player, active=not waiting_for_turn_change
        )

        # Add this line before the if winner
        draw_stats(game_surface, font, match)

        # If there is a winner, show message and count time
        if winner is not None:
            # Show victory message with black text
            BLACK = (0, 0, 0)
            winner_text = font.render(f"¡{winner['name']} ha ganado!", True, WHITE)
            text_rect = winner_text.get_rect()
            text_rect.centerx = game_surface.get_width() // 2
            text_rect.centery = game_surface.get_height() // 2

            # Black background for the victory message
            background = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
            background.set_alpha(160)  # A little more opaque for the victory message
            background.fill((0, 0, 0))
            game_surface.blit(background, (text_rect.x - 20, text_rect.y - 10))
            game_surface.blit(winner_text, text_rect)

            # If 3 seconds have passed, return to menu
            if current_time - winner_show_start_time >= 3:
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load("assets/background_music_menu.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(Settings.get(SettingsKey.VOLUME) * 0.5)
                return

        options_menu.draw(game_surface)

        pygame.display.update()

    # Close Pygame only when you want to exit the game
    pygame.quit()
    sys.exit()
