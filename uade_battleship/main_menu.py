import pygame, sys
import math
import random
from typing import Literal

from .utils import Settings, SettingsKey
from .ui import Button
from .match.match_data import ShipPosition
from .board import board
from .instructions import instructions
from .match import Match, SHIP_SIZES
from .ship_placement import ship_placement

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo de la pantalla
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)  # Blanco para el texto
TRANSLUCENT_BLACK = (0, 0, 0, 128)  # Negro translúcido para superponer sobre el fondo

pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/menu_background.jpg")


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


def play():
    cpu_ships: list[ShipPosition] = []

    def generate_random_ship_position(
        size: int, cpu_ships: list[ShipPosition]
    ) -> ShipPosition:
        # Lista para guardar todas las posiciones válidas
        valid_positions: list[ShipPosition] = []

        # Chequeamos cada celda del tablero
        for y in range(10):
            for x in range(10):
                # Probamos orientación horizontal
                if x + size <= 10:  # Si el barco entra horizontalmente
                    # Creamos el ship para testear
                    ship_horizontal: ShipPosition = {
                        "x": x,
                        "y": y,
                        "size": size,
                        "orientation": "horizontal",
                    }

                    # Conseguimos coordenadas del barco horizontal
                    horizontal_coords = set((x + dx, y) for dx in range(size))

                    # Asumimos que es válida hasta que se demuestre lo contrario
                    valid_horizontal = True

                    # Chequeamos overlap con cada barco existente
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

                # Probamos orientación vertical
                if y + size <= 10:  # Si el barco entra verticalmente
                    ship_vertical: ShipPosition = {
                        "x": x,
                        "y": y,
                        "size": size,
                        "orientation": "vertical",
                    }

                    # Conseguimos coordenadas del barco vertical
                    vertical_coords = set((x, y + dy) for dy in range(size))

                    # Asumimos que es válida hasta que se demuestre lo contrario
                    valid_vertical = True

                    # Chequeamos overlap con cada barco existente
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

        # Si no hay posiciones válidas, lanzamos error
        if not valid_positions:
            raise ValueError("No se encontraron posiciones válidas para el barco")

        # Devolvemos una posición random de las válidas
        return random.choice(valid_positions)

    match = Match("Player", "CPU")

    # Primero vamos a la pantalla de posicionamiento
    if not ship_placement(match):
        return

    for size in SHIP_SIZES:
        ship = generate_random_ship_position(size, cpu_ships)
        cpu_ships.append(ship)
        match.add_ship(1, ship)

    # Luego vamos a la pantalla de juego
    board(match)


def main_menu():
    clock = pygame.time.Clock()
    animation_time = 0  # Variable para controlar el tiempo de animación
    selected_option = 0  # Índice de la opción seleccionada
    mouse_used = False  # Bandera para detectar si el mouse fue usado

    # Definimos la lista de botones
    buttons = [
        Button(
            image=None,
            pos=(640, 200),
            text_input="Comenzar partida",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
        ),
        Button(
            image=None,
            pos=(640, 300),
            text_input="Instrucciones de juego",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
        ),
        Button(
            image=None,
            pos=(640, 400),
            text_input="Configuraciones",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
        ),
        Button(
            image=None,
            pos=(640, 500),
            text_input="Scores",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
        ),
        Button(
            image=None,
            pos=(640, 600),
            text_input="Salir",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
        ),
    ]

    while True:
        screen = pygame.display.get_surface()

        # Dibuja la imagen de fondo y aplica la capa negra translúcida
        background_scaled = pygame.transform.scale(BG, (1280, 720))
        screen.blit(background_scaled, (0, 0))
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill(TRANSLUCENT_BLACK)
        screen.blit(overlay, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Control de la animación: usamos math.sin() para oscilar el tamaño
        animation_time += (
            clock.get_time() / 500
        )  # Dividimos para controlar la velocidad
        scale_factor = 1 + 0.1 * math.sin(
            animation_time
        )  # El factor de escala oscila entre 1 y 1.1
        animated_font_size = int(60 * scale_factor)  # Ajustamos el tamaño de la fuente
        MENU_TEXT = get_font(animated_font_size).render("MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        screen.blit(MENU_TEXT, MENU_RECT)

        # Actualizar colores y posición de botones
        for i, button in enumerate(buttons):
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Mover entre opciones con teclas y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(buttons)
                    mouse_used = False  # Reseteamos el uso del mouse
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(buttons)
                    mouse_used = False  # Reseteamos el uso del mouse
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        play()
                    elif selected_option == 1:
                        instructions()
                    elif selected_option == 4:  # Salir
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mouse_used = True  # Si se mueve el mouse, lo usamos para resaltar
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.checkForInput(MENU_MOUSE_POS):
                        selected_option = i
                        if i == 0:
                            play()
                        elif i == 1:
                            instructions()
                        elif i == 4:
                            pygame.quit()
                            sys.exit()

        # Resaltar la opción seleccionada con el teclado
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
        clock.tick(60)  # Mantenemos una velocidad de 60 FPS


# Cargar música de fondo
pygame.mixer.init()
pygame.mixer.music.load("assets/background_music_menu.mp3")

# Reproducir música de fondo
pygame.mixer.music.play(-1)  # Reproducir en bucle
pygame.mixer.music.set_volume(
    Settings.get(SettingsKey.VOLUME)
)  # Ajustar el volumen al 50%
