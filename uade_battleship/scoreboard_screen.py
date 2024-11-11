import pygame
import sys
from typing import List
from .ui import Button
from .scoreboard import Scoreboard, Score

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo
LIGHT_BLUE = (0, 191, 255)  # Azul claro para hover
WHITE = (255, 255, 255)  # Blanco para texto
GOLD = (255, 215, 0)  # Color para el primer puesto
SILVER = (192, 192, 192)  # Color para el segundo puesto
BRONZE = (205, 127, 50)  # Color para el tercer puesto


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


def scoreboard_screen() -> None:
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Obtener scores
    scores: List[Score] = Scoreboard.get_scoreboard()

    # Crear botón de volver
    back_button = Button(
        image=None,
        pos=(640, 650),
        text_input="Volver al Menú",
        font=get_font(30),
        base_color=DARK_BLUE,
        hovering_color=LIGHT_BLUE,
    )

    while True:
        screen.fill(DARK_BLUE)

        # Título
        title_text = get_font(50).render("MEJORES PUNTAJES", True, WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        screen.blit(title_text, title_rect)

        if not scores:
            # Mensaje cuando no hay scores
            no_scores_text = get_font(30).render(
                "¡Todavía no hay puntajes!", True, WHITE
            )
            no_scores_rect = no_scores_text.get_rect(center=(640, 300))
            screen.blit(no_scores_text, no_scores_rect)

            play_text = get_font(25).render(
                "Jugá una partida para aparecer acá", True, LIGHT_BLUE
            )
            play_rect = play_text.get_rect(center=(640, 350))
            screen.blit(play_text, play_rect)
        else:
            # Ordenar scores por puntaje
            scores.sort(key=lambda x: x["score"])
            # Mostrar los scores
            for i, score in enumerate(scores[:10]):  # Mostrar solo top 10
                # Color según posición
                if i == 0:
                    color = GOLD
                elif i == 1:
                    color = SILVER
                elif i == 2:
                    color = BRONZE
                else:
                    color = WHITE

                # Texto del score
                score_text = get_font(25).render(
                    f"#{i+1}. {score['name']} - {score['score']} puntos", True, color
                )
                score_rect = score_text.get_rect(center=(640, 200 + i * 45))
                screen.blit(score_text, score_rect)

        # Actualizar botón de volver
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        back_button.changeColor(MENU_MOUSE_POS)
        back_button.update(screen)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(MENU_MOUSE_POS):
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(60)
