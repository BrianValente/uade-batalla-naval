import pygame

#inicio de libreria
pygame.init()

#funciones del juego
def CreateGameGrid(rows, cols, cellsize, pos):
    startX = pos[0]
    startY = pos[1]
    coorGrid = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append((startX, startY))
            startX += cellsize  # Mueve hacia la derecha para la siguiente columna
        coorGrid.append(rowX)
        startX = pos[0]  # Resetea startX al inicio de la fila
        startY += cellsize  # Mueve hacia abajo para la siguiente fila
    return coorGrid
        
def updateGameLogic(rows, cols):
    gamelogic = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append(' ')
        gamelogic.append(rowX)
    return gamelogic

def showGridOnScreen(window, cellsize, playerGrid, computerGrid):
    grids = {'Player Grid': playerGrid, 'Computer Grid': computerGrid}
    
    for gridName, grid in grids.items():
        for row in grid:
            for col in row:
                pygame.draw.rect(window, (255, 255, 255), (col[0], col[1], cellsize, cellsize), 1)

def printGameLogic():
    print('Player Grid'.center(50))
    for _ in pGameLogic:
        print(_)
    print('Computer Grid'.center(50))
    for _ in cGameLogic:
        print(_)

def updateGameScreen(window):
    window.fill((0, 0, 0))
    showGridOnScreen(window, CELLSIZE, pGameGrid, cGameGrid)
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

# Inicio de display pygame
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Battleship game')

# Posiciones iniciales de las grillas
pGameGridStartPos = (50, 50)
cGameGridStartPos = (50 + COLS * CELLSIZE + GRID_SPACING, 50)

# Variables del juego
pGameGrid = CreateGameGrid(ROWS, COLS, CELLSIZE, pGameGridStartPos)
pGameLogic = updateGameLogic(ROWS, COLS)

cGameGrid = CreateGameGrid(ROWS, COLS, CELLSIZE, cGameGridStartPos)
cGameLogic = updateGameLogic(ROWS, COLS)

printGameLogic()

# Loop del game
RUNGAME = True
while RUNGAME:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
    
    updateGameScreen(GAMESCREEN)

pygame.quit()



