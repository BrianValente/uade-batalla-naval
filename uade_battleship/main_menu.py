import os
import pygame, sys
import math  # Para la animación
from uade_battleship.board import board
from uade_battleship.instructions import instructions

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo
BRIGHT_BLUE = (30, 144, 255)  # Azul más claro y vibrante para el texto
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón en estado normal
WHITE = (255, 255, 255)  # Blanco para el texto y borde
TRANSLUCENT_BLACK = (0, 0, 0, 128)  # Negro translúcido para superponer sobre el fondo

pygame.display.set_caption("Menu")

# Carga la imagen de fondo desde la carpeta de descargas
BG = pygame.image.load("C:/Users/maria/Downloads/background battleship game menu.jpg")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    board()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen = pygame.display.get_surface()

        # Dibuja la imagen de fondo y aplica la capa negra translúcida
        background_scaled = pygame.transform.scale(BG, (1280, 720))
        screen.blit(background_scaled, (0, 0))
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill(TRANSLUCENT_BLACK)
        screen.blit(overlay, (0, 0))

        OPTIONS_TEXT = get_font(30).render(
            "This is the OPTIONS screen.", True, BRIGHT_BLUE
        )
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 460),
            text_input="BACK",
            font=get_font(30),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    clock = pygame.time.Clock()
    animation_time = 0  # Variable para controlar el tiempo de animación

    while True:
        screen = pygame.display.get_surface()

        # Dibuja la imagen de fondo con capa translúcida
        background_scaled = pygame.transform.scale(BG, (1280, 720))
        screen.blit(background_scaled, (0, 0))
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill(TRANSLUCENT_BLACK)
        screen.blit(overlay, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Control de la animación del texto
        animation_time += clock.get_time() / 500  # Velocidad de la animación
        scale_factor = 1 + 0.1 * math.sin(animation_time)  # Factor de escala

        # Texto "MENU" en BRIGHT_BLUE
        animated_font_size = int(60 * scale_factor)
        MENU_TEXT = get_font(animated_font_size).render("MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        screen.blit(MENU_TEXT, MENU_RECT)

        # Botones con BRIGHT_BLUE para el texto
        PLAY_BUTTON = Button(
            image=None,
            pos=(640, 200),
            text_input="Comenzar partida",
            font=get_font(40),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )
        INSTRUCTIONS_BUTTON = Button(
            image=None,
            pos=(640, 300),
            text_input="Instrucciones de juego",
            font=get_font(40),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )
        CREDITS_BUTTON = Button(
            image=None,
            pos=(640, 400),
            text_input="Configuraciones",
            font=get_font(40),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )
        HELP_BUTTON = Button(
            image=None,
            pos=(640, 500),
            text_input="Scores",
            font=get_font(40),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )
        QUIT_BUTTON = Button(
            image=None,
            pos=(640, 600),
            text_input="Salir",
            font=get_font(40),
            base_color=BRIGHT_BLUE,
            hovering_color=WHITE,
        )

        for button in [
            PLAY_BUTTON,
            INSTRUCTIONS_BUTTON,
            CREDITS_BUTTON,
            HELP_BUTTON,
            QUIT_BUTTON,
        ]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


# Definición de la clase Button sin fondo, con contorno blanco en el texto
class Button:
    def __init__(
        self,
        image,
        pos,
        text_input,
        font,
        base_color,
        hovering_color,
        border_color=WHITE,
        border_thickness=2,
    ):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.update_text()

    def update_text(self, color=None):
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

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        color = (
            self.hovering_color if self.rect.collidepoint(position) else self.base_color
        )
        if color != self.text.get_at((0, 0)):
            self.update_text(color)
