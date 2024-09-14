import pygame
from random import choice, randint

def menu(window, color, font):
    global menu_button_rect
    texto = font.render("Menu", True, (255, 0, 255))
    menu_button_rect = pygame.Rect(20, 20, texto.get_width() + 20, texto.get_height() + 10)
    pygame.draw.rect(window, color, menu_button_rect)
    window.blit(texto, (menu_button_rect.x + 10, menu_button_rect.y + 5))

#muestra el menú
def show_menu(window, font):
    menu_items = ["Volver al Menú Principal"]
    menu_pos = (40, 100)  # Posición del menú

    for idx, item in enumerate(menu_items):
        text = font.render(item, True, (255, 255, 255))
        window.blit(text, (menu_pos[0], menu_pos[1] + idx * 40))
        
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
            orientacion = choice(['H', 'V'])  # Horizontal o Vertical
            if orientacion == 'H':
                fila = randint(0, MAX_ROWS - 1)
                col = randint(0, MAX_COL - barco)
                if all(logica_juego[fila][c] == " " for c in range(col, col + barco)):
                    for c in range(col, col + barco):
                        logica_juego[fila][c] = 'B'  # 'B' representa una parte del barco
                    colocado = True
            else:
                fila = randint(0, MAX_ROWS - barco)
                col = randint(0, MAX_COL - 1)
                if all(logica_juego[f][col] == " " for f in range(fila, fila + barco)):
                    for f in range(fila, fila + barco):
                        logica_juego[f][col] = 'B'
                    colocado = True

# Función para mostrar la grilla en pantalla
def show_grid_on_screen(window, cellsize, player_grid, p_game_logic):
    for row_idx, row in enumerate(player_grid):
        for col_idx, col in enumerate(row):
            if p_game_logic[row_idx][col_idx] == "B":  # Parte del barco
                color = (0, 0, 255)  # Azul para partes del barco
            elif p_game_logic[row_idx][col_idx] == "X":  # Celda seleccionada
                color = (255, 0, 0)  # Rojo para celdas seleccionadas
            elif p_game_logic[row_idx][col_idx] == "M":  # Marcada como fallo
                color = (128, 128, 128)  # Gris para fallos
            else:
                color = (255, 255, 255)  # Blanco para celdas no seleccionadas
            pygame.draw.rect(window, color, (col[0], col[1], cellsize, cellsize))
            pygame.draw.rect(window, (0, 0, 0), (col[0], col[1], cellsize, cellsize), 1)  # Borde de la celda

# Función para imprimir la lógica del juego en la consola
def print_game_logic(p_game_logic):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)

# Función para actualizar la pantalla del juego
def update_game_screen(window, p_game_grid, p_game_logic):
    window.fill((0, 51, 102))
    show_grid_on_screen(window, CELLSIZE, p_game_grid, p_game_logic)
    pygame.display.update()

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
                if p_game_logic[row_idx][col_idx] == 'B':  # Clic en barco
                    p_game_logic[row_idx][col_idx] = "X"  # Marca la celda como acertada
                elif p_game_logic[row_idx][col_idx] == ' ':
                    p_game_logic[row_idx][col_idx] = "M"  # Marca la celda como fallo
                print(f"Clicked on cell ({row_idx}, {col_idx})")
                return  # Salir después del primer clic

# Configuración inicial
ROWS = 10
COLS = 10
CELLSIZE = 40

def board():
    pygame.init()
    GAMESCREEN = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Battleship Game")

    p_game_grid_start_pos = grid_size(GAMESCREEN, ROWS, COLS, CELLSIZE)
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)
    p_game_logic = update_game_logic(ROWS, COLS)

    colocar_barcos(p_game_logic)  # Coloca barcos en la lógica del juego
    print_game_logic(p_game_logic)

    # Inicializar la fuente y el estado del menú
    font = pygame.font.SysFont(None, 36)
    show_menu_flag = False  # Inicialmente, el menú está oculto

    # Crear el rectángulo del botón del menú
    menu_button_rect = pygame.Rect(20, 20, 100, 50)
    
    RUNGAME = True

    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_button_rect.collidepoint(mouse_pos):
                    show_menu_flag = not show_menu_flag
                else:
                    handle_mouse_click(mouse_pos, p_game_grid, CELLSIZE, p_game_logic)

        GAMESCREEN.fill((0, 51, 102))  # Fondo del juego
        # Dibuja el botón del menú
        menu(GAMESCREEN, (100, 100, 100), font)  # Color de fondo del botón

        if show_menu_flag:
            show_menu(GAMESCREEN, font)  # Mostrar el menú
        else:
            update_game_screen(GAMESCREEN, p_game_grid, p_game_logic)  # Mostrar la grilla del juego

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    board()
