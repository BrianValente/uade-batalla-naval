import PySimpleGUI as sg
from random import randint, choice

def colocar_barcos():
    MAX_ROWS = MAX_COL = 10
    barcos = [5, 4, 3, 3, 2]  # Portaaviones, Acorazado, Submarino, Destructor, Patrullero
    tablero = [['O' for _ in range(MAX_COL)] for _ in range(MAX_ROWS)]

    for barco in barcos:
        colocado = False
        while not colocado:
            orientacion = choice(['H', 'V'])  # Horizontal o Vertical
            if orientacion == 'H':
                fila = randint(0, MAX_ROWS - 1)
                col = randint(0, MAX_COL - barco)
                # Verificar que no haya otro barco en el lugar
                if all(tablero[fila][c] == 'O' for c in range(col, col + barco)):
                    for c in range(col, col + barco):
                        tablero[fila][c] = 'B'  # 'B' representa una parte del barco
                    colocado = True
            else:  # Vertical
                fila = randint(0, MAX_ROWS - barco)
                col = randint(0, MAX_COL - 1)
                if all(tablero[f][col] == 'O' for f in range(fila, fila + barco)):
                    for f in range(fila, fila + barco):
                        tablero[f][col] = 'B'
                    colocado = True
    return tablero

def Battleship():
    sg.theme('Dark Blue 1')
    MAX_ROWS = MAX_COL = 10
    # Colocar barcos en el tablero
    tablero = colocar_barcos()
    
    layout = [[sg.Text('BATTLESHIP UADE', font='Default 25')],
              [sg.Text(size=(15, 1), key='-MESSAGE-', font='Default 20')]]
    
    # Crear el tablero
    layout += [[sg.Button('O', size=(4, 2), pad=(0, 0), border_width=0, key=(row, col)) 
                for col in range(MAX_COL)] for row in range(MAX_ROWS)]
    
    # Botón de salida
    layout += [[sg.Button('Exit', button_color=('white', 'red'))]]

    window = sg.Window('Battleship', layout)
    disparos = set()  # Para llevar un registro de las celdas ya disparadas

    while True:
        event, values = window.read()
        
        # Salir del juego
        if event in (None, 'Exit'):
            break
        
        # Verificar si la celda ya fue disparada
        if event not in disparos and isinstance(event, tuple):  # Solo manejar clicks válidos
            disparos.add(event)  # Agregar la celda a las ya disparadas
            if tablero[event[0]][event[1]] == 'B':  # Golpe en el barco
                window[event].update('H', button_color=('white', 'red'))
                window['-MESSAGE-'].update('Hit')
            else:  # Fallo
                window[event].update('M', button_color=('white', 'black'))
                window['-MESSAGE-'].update('Miss')

    window.close()

Battleship()
