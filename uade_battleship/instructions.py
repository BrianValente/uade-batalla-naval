import os
import pygame, sys
from .ui import Button

# Inicializar Pygame
pygame.init()

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo de la pantalla
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)  # Blanco para el texto

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reglas del Juego - Battleship")


# Obtener la fuente personalizada
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


# Clase para los botones


# Función para mostrar las reglas del juego
def instructions():
    while True:
        screen.fill(DARK_BLUE)

        reglas_text = get_font(40).render("REGLAS DEL JUEGO", True, WHITE)
        reglas_rect = reglas_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(reglas_text, reglas_rect)

        # Aquí se pueden añadir más reglas si es necesario

        back_button = Button(
            image=None,
            pos=(WIDTH // 2, HEIGHT // 2 + 100),
            text_input="Volver",
            font=get_font(30),
            base_color=WHITE,
            hovering_color=LIGHT_BLUE,
            bg_color=DARK_BLUE,
            border_color=LIGHT_BLUE,
        )

        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    return

        back_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()
