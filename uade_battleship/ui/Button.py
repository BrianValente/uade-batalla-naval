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
