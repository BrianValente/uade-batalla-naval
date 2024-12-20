import os
import pygame, sys
from typing import List
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
from .ui import Button
from .utils import Color

GAME_RULES: List[str] = [
    "1. Cada jugador tiene un tablero con una cuadrícula de filas y columnas. Los barcos se colocan",
    "   estratégicamente de forma horizontal o vertical (no en diagonal).",
    "2. Los barcos no pueden superponerse ni salirse del tablero.",
    "   ¡La ubicación de tus barcos es un secreto!",
    "3. Por turnos, atacás el tablero enemigo eligiendo una coordenada:",
    "   • GRIS = Agua (no le diste a nada)",
    "   • ROJO = Impacto (le diste a un barco)",
    "   • NEGRO = Barco hundido (le diste a todas sus casillas)",
    "4. Gana el primero en hundir todos los barcos enemigos.",
    "5. Si tu disparo cae en agua, perdés el turno.",
]


def get_font(size: int) -> Font:
    return pygame.font.Font("assets/font.ttf", size)


def instructions() -> None:
    screen = pygame.display.get_surface()
    width, height = screen.get_size()

    while True:
        screen.fill(Color.DARK_BLUE)

        # Title
        rules_text: Surface = get_font(40).render("Instrucciones", True, Color.WHITE)
        rules_rect: Rect = rules_text.get_rect(center=(width // 2, 100))
        screen.blit(rules_text, rules_rect)

        # Show the rules (aligned to the left with a margin of 100px)
        margin_left = 100
        for i, rule in enumerate(GAME_RULES):
            rule_text: Surface = get_font(12).render(rule, True, Color.WHITE)
            rule_rect: Rect = rule_text.get_rect(topleft=(margin_left, 200 + i * 40))
            screen.blit(rule_text, rule_rect)

        # Back button
        back_button: Button = Button(
            image=None,
            pos=(width // 2, height - 75),
            text_input="Volver al Menú",
            font=get_font(30),
            base_color=Color.DARK_BLUE,
            hovering_color=Color.LIGHT_BLUE,
            border_color=Color.WHITE,
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
