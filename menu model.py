import PySimpleGUI as sg

menu_button = ["Menu", ["File", "Edit", "View", "Settings", ["audio", "keyboard", "graphics"]]]

layout = [
    [sg.ButtonMenu( "Menu",menu_def=menu_button)],
    [sg.B("BUtton 1")],
    [sg.B("Button 2", size=(8,4))],
    [sg.Ok(), sg.cancel(button_color="red")]
    ]

window = sg.Window("button app", layout)
event, values = window.read()
print(event, values)