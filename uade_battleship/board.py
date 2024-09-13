import pygame


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


def update_game_logic(rows, cols):
    gamelogic = []
    for _ in range(rows):
        row_x = []
        for _ in range(cols):
            row_x.append(" ")  # Espacio en blanco para celdas vacías
        gamelogic.append(row_x)
    return gamelogic


def show_grid_on_screen(window, cellsize, player_grid, p_game_logic):
    for row_idx, row in enumerate(player_grid):
        for col_idx, col in enumerate(row):
            # Cambiar color de la celda en función de la lógica del juego
            if p_game_logic[row_idx][col_idx] == "X":  # Celda seleccionada
                color = (255, 0, 0)  # Rojo para celdas seleccionadas
                 # Dibuja con borde más grueso para celdas seleccionadas
                pygame.draw.rect(window, color, (col[0], col[1], cellsize, cellsize), 5)
            else:
                color = (255, 255, 255)  # Blanco para celdas no seleccionadas
            pygame.draw.rect(window, color, (col[0], col[1], cellsize, cellsize), 1)


def print_game_logic(p_game_logic):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)


def update_game_screen(window, p_game_grid, p_game_logic):
    window.fill((0, 51, 102))
    show_grid_on_screen(window, CELLSIZE, p_game_grid, p_game_logic)
    pygame.display.update()


def grid_size(window, rows, cols, cellsize):
    """Calcula el tamaño y la posición centrada en la parte inferior de la pantalla"""
    screen_width, screen_height = window.get_size()
    grid_width = cols * cellsize
    grid_height = rows * cellsize
    start_x = (screen_width - grid_width) // 2  # Centrado en X
    start_y = screen_height - grid_height - 50  # 50 píxeles desde la parte inferior
    return start_x, start_y


def handle_mouse_click(mouse_pos, grid, cellsize, p_game_logic):
    """Detecta si se hizo clic en alguna celda de la grilla"""
    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            cell_rect = pygame.Rect(col[0], col[1], cellsize, cellsize)
            if cell_rect.collidepoint(mouse_pos):
                # Actualizar la lógica del juego cuando se hace clic en una celda
                p_game_logic[row_idx][col_idx] = "X"  # Marca la celda como seleccionada
                print(f"Clicked on cell ({row_idx}, {col_idx})")


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

    print_game_logic(p_game_logic)
    RUNGAME = True

    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                handle_mouse_click(mouse_pos, p_game_grid, CELLSIZE, p_game_logic)

        update_game_screen(GAMESCREEN, p_game_grid, p_game_logic)

    pygame.quit()
