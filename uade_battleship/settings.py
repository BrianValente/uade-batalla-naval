import pygame
import sys
from typing import Tuple
from .ui import Button
from .utils import Settings, SettingsKey

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo
LIGHT_BLUE = (0, 191, 255)  # Azul claro para hover
WHITE = (255, 255, 255)  # Blanco para texto
GRAY = (100, 100, 100)  # Gris para la barra de volumen
BLUE = (0, 0, 255)  # Azul para la barra de volumen llena


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font("assets/font.ttf", size)


class VolumeSlider:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_dragging = False

    def draw(self, surface: pygame.Surface):
        # Dibujar barra base
        pygame.draw.rect(surface, GRAY, self.rect)

        # Dibujar barra de volumen
        filled_width = int(Settings.get(SettingsKey.VOLUME) * self.rect.width)
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, filled_width, self.rect.height
        )
        pygame.draw.rect(surface, BLUE, filled_rect)

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

    # Cargar y escalar imagen de volumen
    volume_img = pygame.image.load("assets/volume.png")
    volume_img = pygame.transform.scale(volume_img, (50, 30))

    # Crear slider de volumen
    volume_slider = VolumeSlider(
        x=screen.get_width() // 2 - 150, y=300, width=300, height=20  # Centrado
    )

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
        title_text = get_font(50).render("CONFIGURACIÓN", True, WHITE)
        title_rect = title_text.get_rect(center=(640, 100))
        screen.blit(title_text, title_rect)

        # Texto de volumen
        volume_text = get_font(30).render("Volumen", True, WHITE)
        volume_text_rect = volume_text.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(volume_text, volume_text_rect)

        # Icono de volumen
        screen.blit(volume_img, (volume_slider.rect.x - 60, volume_slider.rect.y - 5))

        # Dibujar slider
        volume_slider.draw(screen)

        # Mostrar porcentaje
        percentage = int(Settings.get(SettingsKey.VOLUME) * 100)
        percentage_text = get_font(25).render(f"{percentage}%", True, WHITE)
        percentage_rect = percentage_text.get_rect(
            midleft=(volume_slider.rect.right + 20, volume_slider.rect.centery)
        )
        screen.blit(percentage_text, percentage_rect)

        # Actualizar botón de volver
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        back_button.changeColor(MENU_MOUSE_POS)
        back_button.update(screen)

        # Eventos
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
