import os
import pygame, sys
from typing import Optional, Union, Tuple
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
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
def get_font(size: int) -> Font:
    return pygame.font.Font("assets/font.ttf", size)


# Clase para los botones
class Button:
    def __init__(
        self,
        image: Optional[Surface],
        pos: Tuple[int, int],
        text_input: str,
        font: Font,
        base_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        hovering_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        bg_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        border_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
    ):
        self.image: Surface = (
            image if image else pygame.Surface((1, 1), pygame.SRCALPHA)
        )
        self.x_pos: int = pos[0]
        self.y_pos: int = pos[1]
        self.font: Font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_input: str = text_input
        self.text: Surface = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text
        self.rect: Rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect: Rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)

    def change_color(self, position: Tuple[int, int]) -> None:
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# Función para mostrar las reglas del juego
def reglas():
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
                    main_menu()

        back_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()
