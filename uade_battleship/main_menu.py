import os
import pygame, sys
import math  # Para la animación

from uade_battleship.board import board
from uade_battleship.match import match

# Colores
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el fondo de la pantalla
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)  # Blanco para el texto

pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    board()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen = pygame.display.get_surface()
        screen.fill(WHITE)  # Fondo blanco para la pantalla de opciones

        OPTIONS_TEXT = get_font(30).render(
            "This is the OPTIONS screen.", True, DARK_BLUE
        )
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 460),
            text_input="BACK",
            font=get_font(30),
            base_color=LIGHT_BLUE,
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
    selected_option = 0  # Índice de la opción seleccionada
    mouse_used = False  # Bandera para detectar si el mouse fue usado

    # Definimos la lista de botones
    buttons = [
        Button(
            image=None,
            pos=(640, 200),
            text_input="Comenzar partida",
            font=get_font(30),
            base_color=LIGHT_BLUE,
            hovering_color=WHITE,
        ),
        Button(
            image=None,
            pos=(640, 300),
            text_input="Instrucciones de juego",
            font=get_font(30),
            base_color=LIGHT_BLUE,
            hovering_color=WHITE,
        ),
        Button(
            image=None,
            pos=(640, 400),
            text_input="Configuraciones",
            font=get_font(30),
            base_color=LIGHT_BLUE,
            hovering_color=WHITE,
        ),
        Button(
            image=None,
            pos=(640, 500),
            text_input="Scores",
            font=get_font(30),
            base_color=LIGHT_BLUE,
            hovering_color=WHITE,
        ),
        Button(
            image=None,
            pos=(640, 600),
            text_input="Salir",
            font=get_font(30),
            base_color=LIGHT_BLUE,
            hovering_color=WHITE,
        ),
    ]

    while True:
        screen = pygame.display.get_surface()
        screen.fill(DARK_BLUE)  # Fondo azul oscuro

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Control de la animación: usamos math.sin() para oscilar el tamaño
        animation_time += (
            clock.get_time() / 500
        )  # Dividimos para controlar la velocidad
        scale_factor = 1 + 0.1 * math.sin(
            animation_time
        )  # El factor de escala oscila entre 1 y 1.1
        animated_font_size = int(60 * scale_factor)  # Ajustamos el tamaño de la fuente
        MENU_TEXT = get_font(animated_font_size).render("MENU", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        screen.blit(MENU_TEXT, MENU_RECT)

        # Actualizar colores y posición de botones
        for i, button in enumerate(buttons):
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Mover entre opciones con teclas y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = (selected_option + 1) % len(buttons)
                    mouse_used = False  # Reseteamos el uso del mouse
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = (selected_option - 1) % len(buttons)
                    mouse_used = False  # Reseteamos el uso del mouse
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        play()
                    elif selected_option == 1:
                        options()
                    elif selected_option == 4:  # Salir
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mouse_used = True  # Si se mueve el mouse, lo usamos para resaltar
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.checkForInput(MENU_MOUSE_POS):
                        selected_option = i
                        if i == 0:
                            play()
                        elif i == 1:
                            options()
                        elif i == 4:
                            pygame.quit()
                            sys.exit()

        # Resaltar la opción seleccionada con el teclado
        if not mouse_used:
            for i, button in enumerate(buttons):
                if i == selected_option:
                    button.text = button.font.render(
                        button.text_input, True, button.hovering_color
                    )
                else:
                    button.text = button.font.render(
                        button.text_input, True, button.base_color
                    )
                button.update(screen)

        pygame.display.update()
        clock.tick(60)  # Mantenemos una velocidad de 60 FPS


# Cargar música de fondo
pygame.mixer.init()
pygame.mixer.music.load("assets/background_music_menu.mp3")

# Reproducir música de fondo
pygame.mixer.music.play(-1)  # Reproducir en bucle
pygame.mixer.music.set_volume(0.5)  # Ajustar el volumen al 50%


# Definición de la clase Button
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        text_width, text_height = self.text.get_size()
        # Adjust button size to fit the text
        self.image = pygame.Surface((text_width + 20, text_height + 20))
        self.image.fill((0, 0, 0, 0))  # Transparent background
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
