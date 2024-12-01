import pygame
from ..utils import Settings, SettingsKey

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

bar_width = 150
bar_height = 20
bar_x = 80
bar_y = 285

menu_button_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
volume_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
adjusting_volume = False


class OptionsMenu:
    def __init__(self):
        self.gear_img = pygame.image.load("assets/gear.png")
        self.gear_img = pygame.transform.scale(self.gear_img, (50, 50))
        self.font = pygame.font.SysFont(None, 36)
        self.ask_return_menu = False
        self.overlay_surface = pygame.Surface(pygame.display.get_surface().get_size())
        self.overlay_surface.set_alpha(140)
        self.overlay_surface.fill((0, 0, 0))

    def draw_menu_button(self, window: pygame.Surface):
        global menu_button_rect
        menu_button_rect = self.gear_img.get_rect(topleft=(20, 20))
        window.blit(self.gear_img, menu_button_rect.topleft)

    def show_menu_options(self, window: pygame.Surface):
        question_text = self.font.render("¿Volver al menú?", True, WHITE)
        yes_text = self.font.render("Sí", True, (0, 150, 0))
        no_text = self.font.render("No", True, (150, 0, 0))

        question_pos = (40, 100)
        yes_button_rect = pygame.Rect(40, 160, 50, 40)
        no_button_rect = pygame.Rect(120, 160, 50, 40)

        pygame.draw.rect(window, GREEN, yes_button_rect)
        pygame.draw.rect(window, RED, no_button_rect)

        window.blit(question_text, question_pos)
        window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
        window.blit(no_text, (no_button_rect.x + 10, no_button_rect.y + 5))

        return yes_button_rect, no_button_rect

    def show_volume_text(self, window: pygame.Surface):
        volume_text = self.font.render("Volumen", True, WHITE)
        window.blit(volume_text, (40, 250))

        volume_img = pygame.image.load("assets/volume.png")
        volume_img = pygame.transform.scale(volume_img, (50, 30))
        window.blit(volume_img, (35, 280))

    def draw_volume_bar(self, window: pygame.Surface):
        pygame.draw.rect(window, GRAY, volume_rect)
        filled_rect = pygame.Rect(
            bar_x, bar_y, int(Settings.get(SettingsKey.VOLUME) * bar_width), bar_height
        )
        pygame.draw.rect(window, BLUE, filled_rect)

    def adjust_volume(self, mouse_x: int, mouse_y: int):
        global adjusting_volume
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            if volume_rect.collidepoint(mouse_x, mouse_y) or adjusting_volume:
                adjusting_volume = True
                volume = (mouse_x - bar_x) / bar_width
                volume = max(0, min(volume, 1))
                pygame.mixer.music.set_volume(volume)
                Settings.set(SettingsKey.VOLUME, volume)
        else:
            adjusting_volume = False

    def handle_click(self, mouse_pos: tuple[int, int]) -> bool:
        """Returns True if should return to menu"""
        if menu_button_rect.collidepoint(mouse_pos):
            self.ask_return_menu = not self.ask_return_menu
            return False

        if self.ask_return_menu:
            yes_button_rect, no_button_rect = self.show_menu_options(
                pygame.display.get_surface()
            )
            if yes_button_rect.collidepoint(mouse_pos):
                pygame.mixer.music.stop()
                pygame.mixer.init()
                pygame.mixer.music.load("assets/background_music_menu.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(Settings.get(SettingsKey.VOLUME))
                return True
            elif no_button_rect.collidepoint(mouse_pos):
                self.ask_return_menu = False

        return False

    def draw(self, window: pygame.Surface):
        self.draw_menu_button(window)

        if self.ask_return_menu:
            window.blit(self.overlay_surface, (0, 0))
            self.show_menu_options(window)
            self.show_volume_text(window)
            self.draw_volume_bar(window)
            self.adjust_volume(*pygame.mouse.get_pos())

    def handle_keyboard(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ask_return_menu = not self.ask_return_menu
