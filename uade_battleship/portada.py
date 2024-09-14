import os
import pygame, sys

from uade_battleship.main_menu import main_menu

pygame.init()

BG = pygame.image.load("assets/Background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    main_menu()


def portada():
    while True:
        screen = pygame.display.get_surface()
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Cambiar texto principal a 'UADE'
        MENU_TEXT = get_font(70).render("UADE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Texto adicional "Battleship: Survival of the greatest"
        SUBTEXT = get_font(30).render(
            "Battleship: Survival of the greatest", True, "#b68f40"
        )
        SUBTEXT_RECT = SUBTEXT.get_rect(center=(640, 200))

        # Cambiar el texto del botón a 'Are you ready? Click here to start the battle!'
        PLAY_BUTTON = Button(
            image=None,  # Eliminamos la imagen
            pos=(640, 400),
            text_input="Are you ready? Click here to start the battle!",
            font=get_font(25),  # Tamaño de texto ajustado
            base_color="#d7fcd4",
            hovering_color="White",
        )

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(SUBTEXT, SUBTEXT_RECT)  # Renderizar el texto adicional

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        PLAY_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

        pygame.display.update()


# button
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Calcular el tamaño del botón basado en el tamaño del texto
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = pygame.Rect(
            0, 0, self.text_rect.width + 40, self.text_rect.height + 20
        )
        self.rect.center = self.x_pos, self.y_pos

    def update(self, screen):
        # Dibujar el botón con un fondo rectangular
        pygame.draw.rect(
            screen, "#b68f40", self.rect, border_radius=12
        )  # Color y bordes del botón
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
