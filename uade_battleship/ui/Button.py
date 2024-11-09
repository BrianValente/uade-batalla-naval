import pygame
from typing import Optional, Union, Tuple
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font


class Button:
    def __init__(
        self,
        image: Optional[Surface],
        pos: Tuple[int, int],
        text_input: str,
        font: Font,
        base_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        hovering_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]],
        border_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]] = (
            255,
            255,
            255,
        ),
        border_thickness: int = 2,
    ):
        self.image: Surface = (
            image if image else pygame.Surface((1, 1), pygame.SRCALPHA)
        )
        self.x_pos: int = pos[0]
        self.y_pos: int = pos[1]
        self.font: Font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input: str = text_input
        self.border_color = border_color
        self.border_thickness: int = border_thickness
        self.text: Surface
        self.rect: Rect
        self.update_text()

    def update_text(
        self,
        color: Optional[Union[Tuple[int, int, int], Tuple[int, int, int, int]]] = None,
    ) -> None:
        # Renderiza el texto con un contorno blanco
        color = color or self.base_color
        self.text = self.font.render(self.text_input, True, color)
        text_width, text_height = self.text.get_size()

        # Crear el fondo del texto para que sea transparente y añadir contorno
        self.image = pygame.Surface(
            (
                text_width + 2 * self.border_thickness,
                text_height + 2 * self.border_thickness,
            ),
            pygame.SRCALPHA,
        )

        # Dibujar el contorno
        for offset_x in range(-self.border_thickness, self.border_thickness + 1):
            for offset_y in range(-self.border_thickness, self.border_thickness + 1):
                if offset_x != 0 or offset_y != 0:
                    contoured_text = self.font.render(
                        self.text_input, True, self.border_color
                    )
                    self.image.blit(
                        contoured_text,
                        (
                            self.border_thickness + offset_x,
                            self.border_thickness + offset_y,
                        ),
                    )

        # Dibujar el texto principal en el centro
        self.image.blit(self.text, (self.border_thickness, self.border_thickness))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def checkForInput(self, position: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)

    def changeColor(self, position: Tuple[int, int]) -> None:
        color = (
            self.hovering_color if self.rect.collidepoint(position) else self.base_color
        )
        if color != self.text.get_at((0, 0)):
            self.update_text(color)
