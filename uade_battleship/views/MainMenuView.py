import arcade
import arcade.gui


class MainMenuView(arcade.View):
    """Class that manages the 'menu' view."""

    def __init__(self, window: arcade.Window):
        super().__init__(window)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        v_box = arcade.gui.UIBoxLayout(space_between=20)

        title = arcade.gui.UILabel(
            text="UADE Battleship",
            font_size=30,
            text_color=arcade.color.BLACK,
        )
        self.start_game_button = arcade.gui.UIFlatButton(
            text="Start Game",
            width=200,
            style={
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.WHITE,
                "border_width": 2,
                "border_color": None,
                "bg_color": (21, 19, 21),
                "bg_color_pressed": arcade.color.WHITE,
                "border_color_pressed": arcade.color.WHITE,
                "font_color_pressed": arcade.color.BLACK,
            },
        )

        v_box.add(title)
        v_box.add(self.start_game_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
            )
        )

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()
