import os
import pygame, sys

from uade_battleship.board import board
from .main_menu import main_menu
from .portada import portada

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))

def main():
    portada()

if __name__ == "__main__":
    main()
