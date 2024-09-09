import pygame


# funciones del juego
def create_game_grid(rows, cols, cellsize, pos):
    start_x = pos[0]
    start_y = pos[1]
    coor_grid = []
    for _ in range(rows):
        row_x = []
        for _ in range(cols):
            row_x.append((start_x, start_y))
            start_x += cellsize  # Mueve hacia la derecha para la siguiente columna
        coor_grid.append(row_x)
        start_x = pos[0]  # Resetea startX al inicio de la fila
        start_y += cellsize  # Mueve hacia abajo para la siguiente fila
    return coor_grid


def update_game_logic(rows, cols):
    gamelogic = []
    for _ in range(rows):
        row_x = []
        for _ in range(cols):
            row_x.append(" ")
        gamelogic.append(row_x)
    return gamelogic


def show_grid_on_screen(window, cellsize, player_grid, computer_grid):
    grids = {"Player Grid": player_grid, "Computer Grid": computer_grid}

    for _, grid in grids.items():
        for row in grid:
            for col in row:
                pygame.draw.rect(
                    window, (255, 255, 255), (col[0], col[1], cellsize, cellsize), 1
                )


def print_game_logic(p_game_logic):
    print("Player Grid".center(50))
    for _ in p_game_logic:
        print(_)
    print("Computer Grid".center(50))
    for _ in p_game_logic:
        print(_)


def update_game_screen(window, p_game_grid, c_game_grid):
    window.fill((0, 0, 0))
    show_grid_on_screen(window, CELLSIZE, p_game_grid, c_game_grid)
    pygame.display.update()


# Configuración de juego visual
ROWS = 10
COLS = 10
CELLSIZE = 30  # Tamaño reducido para que ambas grillas quepan en pantalla

# Espacio entre las dos grillas
GRID_SPACING = 50

# Cálculo del ancho y alto de la pantalla basado en las grillas y su separación
SCREENWIDTH = (COLS * CELLSIZE) * 2 + GRID_SPACING + 100
SCREENHEIGHT = ROWS * CELLSIZE + 100


def board():
    # inicio de libreria
    pygame.init()

    # Inicio de display pygame
    GAMESCREEN = pygame.display.get_surface()
    pygame.display.set_caption("Battleship game")

    # Posiciones iniciales de las grillas
    p_game_grid_start_pos = (50, 50)
    c_game_grid_start_pos = (50 + COLS * CELLSIZE + GRID_SPACING, 50)

    # Variables del juego
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)
    p_game_logic = update_game_logic(ROWS, COLS)

    c_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, c_game_grid_start_pos)

    print_game_logic(p_game_logic)

    # Loop del game
    RUNGAME = True
    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False

        update_game_screen(GAMESCREEN, p_game_grid, c_game_grid)

    pygame.quit()
