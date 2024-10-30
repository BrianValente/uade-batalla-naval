import os
import pygame

from .portada import portada

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
