import os
import pygame, sys
from typing import Optional, Union, Tuple
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
from uade_battleship.main_menu import main_menu

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo de la pantalla
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)  # Blanco para el texto


def get_font(size: int) -> Font:
    return pygame.font.Font("assets/font.ttf", size)


def play() -> None:
    main_menu()


def portada() -> None:
    # Tamaño inicial del texto para el efecto "pop-up"
    title_size: float = 10  # Empieza pequeño
    max_title_size: int = 70  # Tamaño final del texto "UADE"
    growth_rate: float = 0.5  # Velocidad de crecimiento más lenta
    bouncing: bool = False  # Para controlar el efecto de rebote
    bounce_back_rate: float = 0.2  # Velocidad de retroceso en el rebote

    clock: pygame.time.Clock = pygame.time.Clock()

    while True:
        screen: Surface = pygame.display.get_surface()
        screen.fill(DARK_BLUE)

        MENU_MOUSE_POS: Tuple[int, int] = pygame.mouse.get_pos()

        if title_size < max_title_size and not bouncing:
            title_size += growth_rate
        elif title_size >= max_title_size:
            bouncing = True
        if bouncing:
            title_size -= bounce_back_rate
            if title_size <= max_title_size - 5:
                bouncing = False

        MENU_TEXT: Surface = get_font(int(title_size)).render("UADE", True, WHITE)
        MENU_RECT: Rect = MENU_TEXT.get_rect(center=(640, 100))

        SUBTEXT: Surface = get_font(30).render(
            "Battleship: Survival of the greatest", True, WHITE
        )
        SUBTEXT_RECT: Rect = SUBTEXT.get_rect(center=(640, 200))

        PLAY_BUTTON: Button = Button(
            image=None,
            pos=(640, 400),
            text_input="Are you ready? Click here to start the battle!",
            font=get_font(25),
            base_color=WHITE,
            hovering_color=(200, 200, 200),
            bg_color=LIGHT_BLUE,
            border_color=LIGHT_BLUE,
        )

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(SUBTEXT, SUBTEXT_RECT)

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        PLAY_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
            if event.type == pygame.KEYDOWN:
                play()

        pygame.display.update()
        clock.tick(30)


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

        self.text_rect: Rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect: Rect = pygame.Rect(
            0,
            0,
            self.text_rect.width + 20,
            self.text_rect.height + 10,
        )
        self.rect.center = (self.x_pos, self.y_pos)

    def update(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=12)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)

    def changeColor(self, position: Tuple[int, int]) -> None:
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
