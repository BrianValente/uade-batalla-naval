import pygame
import sys
from typing import Tuple
from .ui import Button
from .utils import Settings, SettingsKey, Color


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


class VolumeSlider:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_dragging = False

    def draw(self, surface: pygame.Surface):
        # Draw base bar
        pygame.draw.rect(surface, Color.GRAY, self.rect)

        # Draw volume bar
        filled_width = int(Settings.get(SettingsKey.VOLUME) * self.rect.width)
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, filled_width, self.rect.height
        )
        pygame.draw.rect(surface, Color.BLUE, filled_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self._update_volume(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self._update_volume(event.pos[0])

    def _update_volume(self, mouse_x: int) -> None:
        relative_x = mouse_x - self.rect.x
        volume = max(0, min(1, relative_x / self.rect.width))
        Settings.set(SettingsKey.VOLUME, volume)
        pygame.mixer.music.set_volume(volume)


def settings_screen() -> None:
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Load and scale volume image
    volume_img = pygame.image.load("assets/volume.png")
    volume_img = pygame.transform.scale(volume_img, (50, 30))

    # Create volume slider
    volume_slider = VolumeSlider(
        x=screen.get_width() // 2 - 150, y=300, width=300, height=20  # Centrado
    )

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
        title_text = get_font(50).render("CONFIGURACIÓN", True, Color.WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        screen.blit(title_text, title_rect)

        # Volume text
        volume_text = get_font(30).render("Volumen", True, Color.WHITE)
        volume_text_rect = volume_text.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(volume_text, volume_text_rect)

        # Volume icon
        screen.blit(volume_img, (volume_slider.rect.x - 60, volume_slider.rect.y - 5))

        # Draw slider
        volume_slider.draw(screen)

        # Show percentage
        percentage = int(Settings.get(SettingsKey.VOLUME) * 100)
        percentage_text = get_font(25).render(f"{percentage}%", True, Color.WHITE)
        percentage_rect = percentage_text.get_rect(
            midleft=(volume_slider.rect.right + 20, volume_slider.rect.centery)
        )
        screen.blit(percentage_text, percentage_rect)

        # Update back button
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        back_button.changeColor(MENU_MOUSE_POS)
        back_button.update(screen)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            volume_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(MENU_MOUSE_POS):
                    return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(60)
