import os
import pygame
import sys
from uade_battleship.main_menu import main_menu

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
    try:
        return pygame.font.Font("assets/font.ttf", size)
    except FileNotFoundError:
        return pygame.font.SysFont("Arial", size)  # Usa Arial como alternativa si no se encuentra la fuente

# Clase para los botones
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, bg_color, border_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)  # Borde del botón
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Función para mostrar las reglas del juego
def reglas():
    while True:
        screen.fill(DARK_BLUE)

        # Título de las reglas
        reglas_text = get_font(40).render("REGLAS DEL JUEGO", True, WHITE)
        reglas_rect = reglas_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(reglas_text, reglas_rect)

        # Ejemplo de una regla (puedes agregar más)
        regla1_text = get_font(25).render("1. Destruye todos los barcos enemigos.", True, WHITE)
        regla1_rect = regla1_text.get_rect(center=(WIDTH // 2, 200))
        screen.blit(regla1_text, regla1_rect)

        # Botón "Volver"
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

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    main_menu()

        back_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()
