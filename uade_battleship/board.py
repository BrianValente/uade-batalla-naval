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


player_name = ["Player 1", "CPU"]

# Configuración inicial
ROWS = 10
COLS = 10
CELLSIZE = 40
# Colores
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Variables del volumen
bar_width = 150
bar_height = 20
bar_x = 80  # Coordenada x de la barra
bar_y = 285  # Coordenada y debajo de los botones

menu_button_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)


def draw_menu_button(window: pygame.Surface, gear_img: pygame.Surface):
    global menu_button_rect

    # area del icono de configuración
    menu_button_rect = gear_img.get_rect(topleft=(20, 20))
    window.blit(gear_img, menu_button_rect.topleft)


# Muestra las opciones "¿Volver al menú?" con "Sí" y "No"
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


# Rectángulo que representa la barra de volumen
volume_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)


# Función para dibujar la barra de volumen
def draw_volume_bar(window: pygame.Surface, volume: float):
    # Fondo de la barra (gris)
    pygame.draw.rect(window, GRAY, volume_rect)

    # Parte de la barra que representa el volumen (azul)
    filled_rect = pygame.Rect(bar_x, bar_y, int(volume * bar_width), bar_height)
    pygame.draw.rect(window, BLUE, filled_rect)


# Variable para saber si el mouse está presionando la barra
adjusting_volume = False


# Función para ajustar el volumen al hacer clic y arrastrar
def adjust_volume(mouse_x: int, mouse_y: int):
    global volume, adjusting_volume
    mouse_buttons = pygame.mouse.get_pressed()

    # Verificar si el mouse está dentro de los límites de la barra de volumen
    if mouse_buttons[0]:  # Si el botón izquierdo del mouse está presionado
        if volume_rect.collidepoint(mouse_x, mouse_y) or adjusting_volume:
            adjusting_volume = True
            volume = (mouse_x - bar_x) / bar_width
            volume = max(0, min(volume, 1))  # Limitar entre 0 y 1
            pygame.mixer.music.set_volume(volume)  # Ajustar el volumen de la música
            Settings.set(SettingsKey.VOLUME, volume)
    else:
        adjusting_volume = False  # El usuario soltó el mouse


# Función para crear la grilla
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


# Función para inicializar la lógica del juego
def update_game_logic(rows: int, cols: int):
    gamelogic: list[list[str]] = []
    for _ in range(rows):
        row_x: list[str] = []
        for _ in range(cols):
            row_x.append(" ")  # Espacio en blanco para celdas vacías
        gamelogic.append(row_x)
    return gamelogic


# Función para imprimir la lógica del juego en la consola
def print_game_logic(p_game_logic: list[list[str]]):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)


# Función para calcular el tamaño y la posición de la grilla
def grid_size(window: pygame.Surface, rows: int, cols: int, cellsize: int):
    screen_width, screen_height = window.get_size()
    grid_width = cols * cellsize
    grid_height = rows * cellsize
    start_x = (screen_width - grid_width) // 2  # Centrado en X
    start_y = screen_height - grid_height - 50  # 50 píxeles desde la parte inferior
    return start_x, start_y


# Función para manejar los eventos del teclado
def handle_keyboard_event(event: pygame.event.Event, ask_return_menu: bool):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        ask_return_menu = not ask_return_menu  # Alterna el menú con "Esc"
    return ask_return_menu


def board(match: Match):
    run_game = True

    game_surface = pygame.display.get_surface()
    pygame.display.set_caption("Battleship Game")

    p_game_grid_start_pos = grid_size(game_surface, ROWS, COLS, CELLSIZE)
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)

    # Cargar música de fondo
    pygame.mixer.init()
    pygame.mixer.music.load("assets/background_music_game.mp3")

    # Reproducir música de fondo
    pygame.mixer.music.play(loops=-1)  # Reproducir en bucle
    pygame.mixer.music.set_volume(Settings.get(SettingsKey.VOLUME) * 0.5)  # volumen al 50%

    if not pygame.mixer.get_init():
        print("Error al cargar la música de fondo")

    # Cargar el video de fondo
    video_clip = cast(VideoClipProtocol, VideoFileClip("assets/background.mp4"))
    start_time = time.time()  # Tiempo de inicio de la reproducción

    overlay_surface = pygame.Surface(game_surface.get_size())
    overlay_surface.set_alpha(140)
    overlay_surface.fill((0, 0, 0))

    # Cargar imagen del menú
    gear_img = pygame.image.load("assets/gear.png")
    gear_img = pygame.transform.scale(
        gear_img, (50, 50)
    )  # Ajustar tamaño si es necesario

    # Inicializar la fuente y el estado del menú
    font = pygame.font.SysFont(None, 36)
    ask_return_menu = False  # Controla cuándo mostrar la pregunta de volver al menú

    # Crear una superficie semi-transparente para opacar la grilla
    overlay_surface = pygame.Surface(game_surface.get_size())
    overlay_surface.set_alpha(140)  # 128 es un valor de transparencia (0-255)
    overlay_surface.fill((0, 0, 0))  # Color de la opacidad, en este caso negro

    game_board = GameBoard(match, p_game_grid)
    cpu = CpuAi(match)  # Instanciamos la CPU

    current_player = 0
    waiting_for_turn_change = False
    last_move_time = 0
    winner = None
    winner_show_start_time = 0
    cpu_thinking_start_time = 0  # Para controlar el delay de la CPU
    score_saved = False  # Nueva variable para controlar si ya guardamos el score

    options_menu = OptionsMenu()

    # Cargar los efectos de sonido
    hit_sound = pygame.mixer.Sound("assets/hit.mp3")
    miss_sound = pygame.mixer.Sound("assets/miss.mp3")
    sunk_sound = pygame.mixer.Sound("assets/sunk.mp3")
    
    # Ajustar volumen inicial de los efectos
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
                # Si el ganador es el jugador humano (número 0) y no guardamos el score todavía
                if winner["number"] == 0 and not score_saved:
                    Scoreboard.save_score(
                        {"name": winner["name"], "score": winner["score"]}
                    )
                    score_saved = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()  # Cerramos Pygame al cerrar la ventana
                sys.exit()  # Cerramos el programa

            options_menu.handle_keyboard(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if options_menu.handle_click(mouse_pos):
                    return  # Volver al menú

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
        ):  # Turno de la CPU
            if cpu_thinking_start_time == 0:  # Si recién empieza el turno de la CPU
                cpu_thinking_start_time = current_time
            elif current_time - cpu_thinking_start_time >= 1:  # Si ya pasó 1 segundo
                shot_result = cpu.play_turn()
                if shot_result == ShotResult.MISS:
                    miss_sound.play()
                    waiting_for_turn_change = True
                    last_move_time = current_time
                elif shot_result == ShotResult.HIT:
                    hit_sound.play()
                elif shot_result == ShotResult.SUNK:
                    sunk_sound.play()
                cpu_thinking_start_time = 0  # Reseteamos para el próximo turno

        # Check if 2 seconds have passed since the last move
        if waiting_for_turn_change and current_time - last_move_time >= 2:
            current_player = 1 - current_player
            waiting_for_turn_change = False

        # Reproducir el video de fondo
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

        # Mostrar el engranaje de configuración
        draw_menu_button(game_surface, gear_img)

        # Draw the current player title centered at the top
        current_player_text = font.render(
            f"Turno de {player_name[current_player]}", True, WHITE
        )
        text_rect = current_player_text.get_rect()
        text_rect.centerx = game_surface.get_width() // 2
        text_rect.top = 10
        game_surface.blit(current_player_text, text_rect)

        game_board.draw_enemy_board(
            game_surface, enemy_player=enemy_player, active=not waiting_for_turn_change
        )

        # If there is a winner, show message and count time
        if winner is not None:
            # Show victory message with black text
            BLACK = (0, 0, 0)
            winner_text = font.render(
                f"¡{player_name[winner['number']]} ha ganado!", True, BLACK
            )
            text_rect = winner_text.get_rect()
            text_rect.centerx = game_surface.get_width() // 2
            text_rect.centery = game_surface.get_height() // 2
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

    # Cerrar Pygame solo cuando se desee salir del juego
    pygame.quit()
    sys.exit()
