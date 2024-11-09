import os
import pygame, sys
from typing import Optional, Union, Tuple, List
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
from .ui import Button

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo de la pantalla
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)  # Blanco para el texto

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reglas del Juego - Battleship")

# Reglas del juego (textos más cortos y concisos)
GAME_RULES: List[str] = [
    "• Tablero de 10x10 para cada jugador",
    "• Barcos de 3 a 6 casillas",
    "• Colocación horizontal o vertical",
    "• Click en el tablero enemigo para disparar",
    "• Rojo = Impacto | Gris = Agua | Negro = Barco enemigo hundido",
    "• Gana quien hunda todos los barcos enemigos",
    "• ¡Usá estrategia para ganar!",
]


def get_font(size: int) -> Font:
    return pygame.font.Font("assets/font.ttf", size)


def instructions() -> None:
    while True:
        screen.fill(DARK_BLUE)

        # Título
        reglas_text: Surface = get_font(40).render("REGLAS DEL JUEGO", True, WHITE)
        reglas_rect: Rect = reglas_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(reglas_text, reglas_rect)

        # Mostrar las reglas (centradas y con menos espacio vertical)
        for i, rule in enumerate(GAME_RULES):
            rule_text: Surface = get_font(18).render(rule, True, WHITE)
            rule_rect: Rect = rule_text.get_rect(center=(WIDTH // 2, 200 + i * 40))
            screen.blit(rule_text, rule_rect)

        # Botón de volver
        back_button: Button = Button(
            image=None,
            pos=(WIDTH // 2, HEIGHT - 100),
            text_input="Volver al Menú",
            font=get_font(30),
            base_color=DARK_BLUE,
            hovering_color=LIGHT_BLUE,
            border_color=WHITE,
        )

        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.checkForInput(mouse_pos):
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        back_button.changeColor(pygame.mouse.get_pos())

        pygame.display.update()
