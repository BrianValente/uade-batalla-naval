import os
import pygame, sys

from uade_battleship.board import board
from .main_menu import main_menu
from .portada import portada
from uade_battleship.match import match

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

# Cargar el icono
icon_path = os.path.join("assets", "icon.png")
icon = pygame.image.load(icon_path)
icon = pygame.transform.scale(icon, (64, 64))  # se redimensiona el icono
# configurar el icono de la ventana
pygame.display.set_icon(icon)


def main():
    portada()


if __name__ == "__main__":
    main()
