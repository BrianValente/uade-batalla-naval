import arcade

from uade_battleship.views import MainMenuView

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "UADE Battleship"


class MainWindow(arcade.Window):
    perf_graph = arcade.PerfGraph(
        width=SCREEN_WIDTH // 4,
        height=100,
    )

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.enable_timings()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        super().on_draw()
        self.perf_graph.draw()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.perf_graph.update_graph(delta_time)


def main():
    window = MainWindow()
    menu_view = MainMenuView(window)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
