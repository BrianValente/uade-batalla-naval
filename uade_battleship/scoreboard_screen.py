import pygame
import sys
from typing import List
from .ui import Button
from .scoreboard import Scoreboard, Score
from .utils import Color


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


def scoreboard_screen() -> None:
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Get scores
    scores: List[Score] = Scoreboard.get_scoreboard()

    # Create back button
    back_button = Button(
        image=None,
        pos=(640, 650),
        text_input="Volver al Menú",
        font=get_font(30),
        base_color=Color.DARK_BLUE,
        hovering_color=Color.LIGHT_BLUE,
    )

    while True:
        screen.fill(Color.DARK_BLUE)

        # Title
        title_text = get_font(50).render("Mejores Puntajes", True, Color.WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        screen.blit(title_text, title_rect)

        if not scores:
            # Message when there are no scores
            no_scores_text = get_font(30).render(
                "¡Todavía no hay puntajes!", True, Color.WHITE
            )
            no_scores_rect = no_scores_text.get_rect(center=(640, 300))
            screen.blit(no_scores_text, no_scores_rect)

            play_text = get_font(25).render(
                "Jugá una partida para aparecer acá", True, Color.LIGHT_BLUE
            )
            play_rect = play_text.get_rect(center=(640, 350))
            screen.blit(play_text, play_rect)
        else:
            # Sort scores by score
            scores.sort(key=lambda x: x["score"])
            # Show scores
            for i, score in enumerate(scores[:10]):  # Show only top 10
                # Color according to position
                if i == 0:
                    color = Color.GOLD
                elif i == 1:
                    color = Color.SILVER
                elif i == 2:
                    color = Color.BRONZE
                else:
                    color = Color.WHITE

                # Score text
                score_text = get_font(25).render(
                    f"#{i+1}. {score['name']} - {score['score']} puntos", True, color
                )
                score_rect = score_text.get_rect(center=(640, 200 + i * 45))
                screen.blit(score_text, score_rect)

        # Update back button
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        back_button.changeColor(MENU_MOUSE_POS)
        back_button.update(screen)

        # Events
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
