import pygame, sys
import math
import random
from typing import Literal

from .utils import Settings, SettingsKey
from .ui import Button
from .match.match_data import ShipPosition
from .board import board
from .instructions import instructions
from .match import Match

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
    # Implementación temporal para testing
    def generate_random_ship() -> ShipPosition:
        """Genera un barco random con tamaño entre 3 y 6"""
        attempts = 0
        while attempts < 100:  # Límite de intentos para evitar loop infinito
            try:
                size = random.randint(3, 6)
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation: Literal["horizontal", "vertical"] = random.choice(
                    ["horizontal", "vertical"]
                )

                ship: ShipPosition = {
                    "x": x,
                    "y": y,
                    "size": size,
                    "orientation": orientation,
                }
                return ship
            except ValueError:
                attempts += 1
                continue
        raise Exception("No se pudo generar un barco válido después de 100 intentos")

    match = Match("Player", "CPU")

    # Generamos 5 barcos random para cada jugador
    for player in [0, 1]:  # Player 0 y CPU (player 1)
        ships_added = 0
        attempts = 0

        while ships_added < 10 and attempts < 100:  # 5 barcos por jugador
            try:
                ship = generate_random_ship()
                match.add_ship(player, ship)
                ships_added += 1
            except (
                ValueError
            ):  # Si hay overlap o está fuera de bounds, intentamos de nuevo
                attempts += 1
                continue

        if ships_added < 5:
            raise Exception(
                f"No se pudieron generar 5 barcos válidos para el jugador {player}"
            )

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
