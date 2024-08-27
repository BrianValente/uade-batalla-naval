import arcade

from uade_battleship.utils import Suma

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "UADE Battleship"
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.ALMOND)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""
        # Clear the screen
        self.clear()

        resultado = Suma(1, 2)
        start_x = 0
        start_y = SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5
        arcade.draw_text(
            f"El resultado de 1 + 2 es {resultado}",
            start_x,
            start_y,
            arcade.color.BLACK,
            DEFAULT_FONT_SIZE * 2,
            width=SCREEN_WIDTH,
            align="center",
        )

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """Called when the user presses a mouse button."""
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """User moves mouse"""
        pass


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
