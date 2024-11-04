import pygame, sys
from uade_battleship.main_menu import main_menu

pygame.init()

# Colores
LIGHT_BLUE = (0, 191, 255)  # Azul claro para el botón y su borde
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
# Blanco para el texto

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    main_menu()

def portada():
    # Cargar la imagen de fondo
    try:
        background_image = pygame.image.load(r"C:\Users\maria\Downloads\background portada.jpg")
        background_image = pygame.transform.scale(background_image, (1280, 720))  # Ajusta el tamaño al de la pantalla
    except pygame.error as e:
        print(f"Error al cargar la imagen: {e}")
        sys.exit()

    # Tamaño inicial del texto para el efecto "pop-up"
    title_size = 10  # Empieza pequeño
    max_title_size = 70  # Tamaño final del texto "UADE"
    growth_rate = 0.5  # Velocidad de crecimiento más lenta
    bouncing = False  # Para controlar el efecto de rebote
    bounce_back_rate = 0.2  # Velocidad de retroceso en el rebote

    clock = pygame.time.Clock()  # Reloj para controlar los FPS y la velocidad

    while True:
        screen = pygame.display.get_surface()

        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Aumenta gradualmente el tamaño del texto "UADE"
        if title_size < max_title_size and not bouncing:
            title_size += growth_rate
        elif title_size >= max_title_size:
            bouncing = True
        if bouncing:
            title_size -= bounce_back_rate
            if title_size <= max_title_size - 5:  # Pequeño rebote al final
                bouncing = False

        # Cambiar texto principal a 'UADE' con color blanco
        MENU_TEXT = get_font(int(title_size)).render("UADE", True, DARK_BLUE)  # Color blanco
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Texto adicional "Battleship: Survival of the greatest" en color blanco
        SUBTEXT = get_font(30).render("Battleship: Survival of the greatest", True, WHITE)
        SUBTEXT_RECT = SUBTEXT.get_rect(center=(640, 200))

        # Botón estático (sin animación)
        PLAY_BUTTON = Button(
            image=None,  # Eliminamos la imagen
            pos=(640, 400),  # Posición fija del botón en el centro
            text_input="Are you ready? Click here to start the battle!",
            font=get_font(25),  # Tamaño de texto del botón
            base_color=WHITE,  # Texto del botón en blanco
            hovering_color=(200, 200, 200),  # Color al pasar el mouse por encima (gris claro)
            bg_color=LIGHT_BLUE,  # Fondo del botón azul claro
            border_color=LIGHT_BLUE,  # Borde del botón azul claro (igual al fondo del botón)
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
            if event.type == pygame.KEYDOWN:
                play()

        pygame.display.update()

        # Controlar los FPS para hacer la animación más suave
        clock.tick(30)  # Esto hace que la animación corra a 30 FPS

# button
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, bg_color, border_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.bg_color = bg_color  # Color de fondo del botón (ahora azul claro)
        self.border_color = border_color  # Color del borde del botón (igual al fondo)
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Calcular el tamaño del botón basado en el tamaño del texto
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rect = pygame.Rect(
            0, 0, self.text_rect.width + 20, self.text_rect.height + 10  # Reducimos el tamaño del botón
        )
        self.rect.center = self.x_pos, self.y_pos

    def update(self, screen):
        # Dibujar el botón con fondo azul claro, borde azul claro y bordes redondeados
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=12)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



