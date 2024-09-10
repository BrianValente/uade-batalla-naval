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
            row_x.append(" ")
        gamelogic.append(row_x)
    return gamelogic

def show_grid_on_screen(window, cellsize, player_grid):
    for row in player_grid:
        for col in row:
            pygame.draw.rect(window, (255, 255, 255), (col[0], col[1], cellsize, cellsize), 1)

def print_game_logic(p_game_logic):
    print("Player Grid".center(50))
    for row in p_game_logic:
        print(row)

def update_game_screen(window, p_game_grid):
    window.fill((0, 51, 102))
    show_grid_on_screen(window, CELLSIZE, p_game_grid)
    pygame.display.update()

ROWS = 10
COLS = 10
CELLSIZE = 30
SCREENWIDTH = COLS * CELLSIZE + 100
SCREENHEIGHT = ROWS * CELLSIZE + 100

def board():
    pygame.init()
    GAMESCREEN = pygame.display.get_surface()
    pygame.display.set_caption("Battleship Game")
    p_game_grid_start_pos = (50, 50)
    p_game_grid = create_game_grid(ROWS, COLS, CELLSIZE, p_game_grid_start_pos)
    p_game_logic = update_game_logic(ROWS, COLS)
    print_game_logic(p_game_logic)
    RUNGAME = True
    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
        update_game_screen(GAMESCREEN, p_game_grid)
    pygame.quit()
