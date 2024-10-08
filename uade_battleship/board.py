import pygame
import subprocess  # Para ejecutar main.py
from random import choice, randint


def draw_menu_button(window, color, font):
    global menu_button_rect
    texto = font.render("Menu", True, (255, 0, 255))
    menu_button_rect = pygame.Rect(
        20, 20, texto.get_width() + 20, texto.get_height() + 10
    )
    pygame.draw.rect(window, color, menu_button_rect)
    window.blit(texto, (menu_button_rect.x + 10, menu_button_rect.y + 5))


# Muestra las opciones "¿Volver al menú?" con "Sí" y "No"
def show_menu_options(window, font):
    question_text = font.render("¿Volver al menú?", True, (255, 255, 255))
    yes_text = font.render("Sí", True, (0, 150, 0))
    no_text = font.render("No", True, (150, 0, 0))

    question_pos = (40, 100)
    yes_button_rect = pygame.Rect(40, 160, 50, 40)
    no_button_rect = pygame.Rect(120, 160, 50, 40)

    pygame.draw.rect(window, (0, 255, 0), yes_button_rect)
    pygame.draw.rect(window, (255, 0, 0), no_button_rect)

    window.blit(question_text, question_pos)
    window.blit(yes_text, (yes_button_rect.x + 10, yes_button_rect.y + 5))
    window.blit(no_text, (no_button_rect.x + 10, no_button_rect.y + 5))

    return yes_button_rect, no_button_rect


# Función para crear la grilla
def create_game_grid(rows, cols, cellsize, pos):
    start_x = pos[0]
    start_y = pos[1]
    coor_grid = []
    for _ in range(rows):
        row_x = []
        for _ in range(cols):
            row_x.append((start_x, start_y))
            start_x += cellsize
        coor_grid.append(row_x)
        start_x = pos[0]
        start_y += cellsize
    return coor_grid


# Función para inicializar la lógica del juego
def update_game_logic(rows, cols):
    gamelogic = []
    for _ in range(rows):
        row_x = []
        for _ in range(cols):
            row_x.append(" ")  # Espacio en blanco para celdas vacías
        gamelogic.append(row_x)
    return gamelogic


# Función para colocar barcos en la lógica del juego
def colocar_barcos(logica_juego):
    MAX_ROWS = MAX_COL = len(logica_juego)
    barcos = [5, 4, 3, 3, 2]  # Tamaños de los barcos

    for barco in barcos:
        colocado = False
        while not colocado:
            orientacion = choice(["H", "V"])  # Horizontal o Vertical
            if orientacion == "H":
                fila = randint(0, MAX_ROWS - 1)
                col = randint(0, MAX_COL - barco)
                if all(logica_juego[fila][c] == " " for c in range(col, col + barco)):
                    for c in range(col, col + barco):
                        logica_juego[fila][
                            c
                        ] = "B"  # 'B' representa una parte del barco
                    colocado = True
            else:
                fila = randint(0, MAX_ROWS - barco)
                col = randint(0, MAX_COL - 1)
                if all(logica_juego[f][col] == " " for f in range(fila, fila + barco)):
                    for f in range(fila, fila + barco):
                        logica_juego[f][col] = "B"
                    colocado = True


# Función para mostrar la grilla en pantalla
def show_grid_on_screen(window, cellsize, player_grid, p_game_logic):
    # Dibujar las celdas de la grilla
    for row_idx, row in enumerate(player_grid):
        for col_idx, col in enumerate(row):
            if p_game_logic[row_idx][col_idx] == "B":  # Parte del barco
                color = (0, 0, 250)  # Azul para partes del barco
            elif p_game_logic[row_idx][col_idx] == "X":  # Celda seleccionada
                color = (255, 0, 0)  # Rojo para celdas seleccionadas
            elif p_game_logic[row_idx][col_idx] == "M":  # Marcada como fallo
                color = (128, 128, 128)  # Gris para fallos
            else:
                color = (255, 255, 255)  # Blanco para celdas no seleccionadas
            pygame.draw.rect(window, color, (col[0], col[1], cellsize, cellsize))
            pygame.draw.rect(
                window, (0, 0, 0), (col[0], col[1], cellsize, cellsize), 1
            )  # Borde de la celda

    # Añadir el primer borde alrededor de toda la grilla
    grid_width = len(player_grid[0]) * cellsize  # Ancho total de la grilla
    grid_height = len(player_grid) * cellsize  # Altura total de la grilla
    top_left_x = player_grid[0][0][0]  # X de la esquina superior izquierda
    top_left_y = player_grid[0][0][1]  # Y de la esquina superior izquierda

    # Dibujar el primer borde de la grilla (el más interno)
    pygame.draw.rect(
        window, (0, 0, 0), (top_left_x, top_left_y, grid_width, grid_height), 1
    )  # 3 es el grosor del borde

    # Añadir el segundo borde, más grande
    second_border_padding = 10  # Distancia entre el primer borde y el segundo
    second_border_width = (
        grid_width + 2 * second_border_padding
    )  # Ancho del segundo borde
    second_border_height = (
        grid_height + 2 * second_border_padding
    )  # Altura del segundo borde
    second_top_left_x = (
        top_left_x - second_border_padding
    )  # Ajustar la posición X del segundo borde
    second_top_left_y = (
        top_left_y - second_border_padding
    )  # Ajustar la posición Y del segundo borde

    # Dibujar el segundo borde (más externo)
    pygame.draw.rect(
        window,
        (150, 0, 150),
        (
            second_top_left_x,
            second_top_left_y,
            second_border_width,
            second_border_height,
        ),
        6,
    )  # 3 es el grosor del segundo borde

    # Añadir el primer borde alrededor de toda la grilla
    grid_width = len(player_grid[0]) * cellsize  # Ancho total de la grilla
    grid_height = len(player_grid) * cellsize  # Altura total de la grilla
    top_left_x = player_grid[0][0][0]  # X de la esquina superior izquierda
    top_left_y = player_grid[0][0][1]  # Y de la esquina superior izquierda

    # Dibujar el primer borde de la grilla (el más interno)
    pygame.draw.rect(
        window, (0, 0, 0), (top_left_x, top_left_y, grid_width, grid_height), 1
    )  # 3 es el grosor del borde

    # Añadir el segundo borde, más grande
    second_border_padding = 10  # Distancia entre el primer borde y el segundo
    second_border_width = (
        grid_width + 2 * second_border_padding
    )  # Ancho del segundo borde
    second_border_height = (
        grid_height + 2 * second_border_padding
    )  # Altura del segundo borde
    second_top_left_x = (
        top_left_x - second_border_padding
    )  # Ajustar la posición X del segundo borde
    second_top_left_y = (
        top_left_y - second_border_padding
    )  # Ajustar la posición Y del segundo borde

    # Dibujar el segundo borde (más externo)
    pygame.draw.rect(
        window,
        (150, 0, 150),
        (
            second_top_left_x,
            second_top_left_y,
            second_border_width,
            second_border_height,
        ),
        6,
    )  # 3 es el grosor del segundo borde


# Función para imprimir la lógica del juego en la consola
def print_game_logic(p_game_logic):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)


# Función para actualizar la pantalla del juego
def update_game_screen(window, p_game_grid, p_game_logic):
    show_grid_on_screen(window, CELLSIZE, p_game_grid, p_game_logic)


# Función para calcular el tamaño y la posición de la grilla
def grid_size(window, rows, cols, cellsize):
    screen_width, screen_height = window.get_size()
    grid_width = cols * cellsize
    grid_height = rows * cellsize
    start_x = (screen_width - grid_width) // 2  # Centrado en X
    start_y = screen_height - grid_height - 50  # 50 píxeles desde la parte inferior
    return start_x, start_y


# Función para manejar los clics del ratón
def handle_mouse_click(mouse_pos, grid, cellsize, p_game_logic):
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            cell_rect = pygame.Rect(col[0], col[1], cellsize, cellsize)
            if cell_rect.collidepoint(mouse_pos):
                if p_game_logic[row_idx][col_idx] == "B":  # Clic en barco
                    p_game_logic[row_idx][col_idx] = "X"  # Marca la celda como acertada
                elif p_game_logic[row_idx][col_idx] == " ":
                    p_game_logic[row_idx][col_idx] = "M"  # Marca la celda como fallo
                print(f"Clicked on cell ({row_idx}, {col_idx})")
                return  # Salir después del primer clic


# Configuración inicial
ROWS = 10
COLS = 10
CELLSIZE = 40


def board():
    pygame.init()
    GAMESCREEN = pygame.display.get_surface()
    pygame.display.set_caption("Battleship Game")

    p_game_grid_start_pos = grid_size(GAMESCREEN, ROWS, COLS, CELLSIZE)
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)
    p_game_logic = update_game_logic(ROWS, COLS)

    colocar_barcos(p_game_logic)  # Coloca barcos en la lógica del juego
    print_game_logic(p_game_logic)

    # Inicializar la fuente y el estado del menú
    font = pygame.font.SysFont(None, 36)
    ask_return_menu = False  # Controla cuándo mostrar la pregunta de volver al menú

    # Crear una superficie semi-transparente para opacar la grilla
    overlay_surface = pygame.Surface(GAMESCREEN.get_size())
    overlay_surface.set_alpha(140)  # 128 es un valor de transparencia (0-255)
    overlay_surface.fill((0, 0, 0))  # Color de la opacidad, en este caso negro

    RUNGAME = True

    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_button_rect.collidepoint(mouse_pos):
                    ask_return_menu = (
                        not ask_return_menu
                    )  # Alternar la visibilidad del menú
                if ask_return_menu:
                    yes_button_rect, no_button_rect = show_menu_options(
                        GAMESCREEN, font
                    )
                    if yes_button_rect.collidepoint(mouse_pos):
                        return
                    elif no_button_rect.collidepoint(mouse_pos):
                        ask_return_menu = False  # Ocultar el menú y volver al juego
                else:
                    handle_mouse_click(mouse_pos, p_game_grid, CELLSIZE, p_game_logic)

        GAMESCREEN.fill((0, 51, 102))  # Fondo del juego

        # Mostrar siempre el botón del menú
        draw_menu_button(GAMESCREEN, (100, 100, 100), font)

        update_game_screen(
            GAMESCREEN, p_game_grid, p_game_logic
        )  # Mostrar la grilla del juego

        if ask_return_menu:
            GAMESCREEN.blit(overlay_surface, (0, 0))  # Añadir la capa opaca
            show_menu_options(GAMESCREEN, font)  # Mostrar opciones Sí/No

        pygame.display.update()


if __name__ == "__main__":
    board()
