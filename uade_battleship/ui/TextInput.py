import pygame
from pygame import Surface


class TextInput:
    def __init__(
        self,
        pos: tuple[int, int],
        font: pygame.font.Font,
        text: str = "",
        base_color: tuple[int, int, int] = (255, 255, 255),
        selected_color: tuple[int, int, int] = (0, 255, 0),
    ):
        self.pos = pos
        self.font = font
        self.text = text
        self.base_color = base_color
        self.selected_color = selected_color
        self.selected = False
        self.max_length = 20

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked inside text input
            text_surface = self.font.render(self.text, True, self.base_color)
            text_rect = text_surface.get_rect(center=self.pos)
            text_rect.inflate_ip(20, 20)  # Make clickable area a bit larger
            self.selected = text_rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.selected:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.selected = False
            elif len(self.text) < self.max_length:
                self.text += event.unicode

    def draw(self, screen: Surface):
        color = self.selected_color if self.selected else self.base_color
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.pos)

        # Draw background rect when selected
        if self.selected:
            bg_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, (50, 50, 50), bg_rect)
            pygame.draw.rect(screen, color, bg_rect, 2)

        screen.blit(text_surface, text_rect)

    def get_text(self) -> str:
        return self.text
