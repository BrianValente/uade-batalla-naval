from typing import TypeAlias
import pygame

from ..match import Match, MatchCellState, ShotResult

BoardPosition: TypeAlias = list[list[tuple[int, int]]]
CELL_SIZE = 40


class GameBoard:
    def __init__(self, match: Match, board_position: BoardPosition) -> None:
        self.match = match
        self.board_position = board_position

    def draw_enemy_board(
        self, surface: pygame.Surface, enemy_player: int, active: bool = True
    ):
        """
        Draw the enemy board.

        Args:
            surface (pygame.Surface): The surface to draw on.
            enemy_player (int): The enemy player to draw the board for (0 or 1).
            active (bool): Whether the board is active or not.
        """
        temp_surface = pygame.Surface(
            (surface.get_width(), surface.get_height()), pygame.SRCALPHA
        )

        board = self.match.get_board(enemy_player)
        sunken_ships = self.match.get_sunken_ships(enemy_player)
        sunken_coords = [coord for ship in sunken_ships for coord in ship]

        for row_i, row in enumerate(board):
            for col_i, cell in enumerate(row):
                if {"x": col_i, "y": row_i} in sunken_coords:
                    color = (0, 0, 0)  # Black for sunken ships
                elif cell == MatchCellState.HIT:
                    color = (255, 0, 0)  # Red for hits
                elif cell == MatchCellState.MISS:
                    color = (128, 128, 128)
                else:
                    color = (255, 255, 255)

                # If not active, add transparency
                if not active:
                    color = (*color, 192)  # Add alpha of 192 (25% transparent)
                else:
                    color = (*color, 255)  # Fully opaque

                grid_pos = self.board_position[row_i][col_i]
                pygame.draw.rect(
                    temp_surface,
                    color,
                    (grid_pos[0], grid_pos[1], CELL_SIZE, CELL_SIZE),
                )
                border_color = (0, 0, 0, 192) if not active else (0, 0, 0, 255)
                pygame.draw.rect(
                    temp_surface,
                    border_color,
                    (grid_pos[0], grid_pos[1], CELL_SIZE, CELL_SIZE),
                    1,
                )

        # Add first border around the entire grid
        grid_width = len(self.board_position[0]) * CELL_SIZE  # Total grid width
        grid_height = len(self.board_position) * CELL_SIZE  # Total grid height
        top_left_x = self.board_position[0][0][0]  # X of top-left corner
        top_left_y = self.board_position[0][0][1]  # Y of top-left corner

        # Draw the first grid border (innermost)
        pygame.draw.rect(
            surface, (0, 0, 0), (top_left_x, top_left_y, grid_width, grid_height), 1
        )  # Border thickness is 1

        # Add second border, larger
        second_border_padding = 10  # Distance between first and second border
        second_border_width = (
            grid_width + 2 * second_border_padding
        )  # Second border width
        second_border_height = (
            grid_height + 2 * second_border_padding
        )  # Second border height
        second_top_left_x = (
            top_left_x - second_border_padding
        )  # Adjust X position of second border
        second_top_left_y = (
            top_left_y - second_border_padding
        )  # Adjust Y position of second border

        # Draw the second border (outermost)
        pygame.draw.rect(
            surface,
            (150, 0, 150),
            (
                second_top_left_x,
                second_top_left_y,
                second_border_width,
                second_border_height,
            ),
            6,
        )  # Border thickness is 6

        # Add first border around the entire grid
        grid_width = len(self.board_position[0]) * CELL_SIZE  # Total grid width
        grid_height = len(self.board_position) * CELL_SIZE  # Total grid height
        top_left_x = self.board_position[0][0][0]  # X of top-left corner
        top_left_y = self.board_position[0][0][1]  # Y of top-left corner

        # Draw the first grid border (innermost)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (top_left_x, top_left_y, grid_width, grid_height),
            width=1,
        )

        # Add second border, larger
        second_border_padding = 10  # Distance between first and second border
        second_border_width = (
            grid_width + 2 * second_border_padding
        )  # Second border width
        second_border_height = (
            grid_height + 2 * second_border_padding
        )  # Second border height
        second_top_left_x = (
            top_left_x - second_border_padding
        )  # Adjust X position of second border
        second_top_left_y = (
            top_left_y - second_border_padding
        )  # Adjust Y position of second border

        # Draw the second border (outermost)
        pygame.draw.rect(
            surface,
            (150, 0, 150),
            (
                second_top_left_x,
                second_top_left_y,
                second_border_width,
                second_border_height,
            ),
            width=6,
        )

        # Finally, we draw the temporary surface onto the main surface
        surface.blit(temp_surface, (0, 0))

    def handle_click(
        self, mouse_pos: tuple[int, int], player: int
    ) -> ShotResult | None:
        """
        Handle a click on the board.

        Args:
            mouse_pos (tuple[int, int]): The position of the mouse click.
            player (int): The player that made the click.

        Returns:
            None: If the shot was invalid.
            ShotResult: The result of the shot.
        """
        for row_idx, row in enumerate(self.board_position):
            for col_idx, col in enumerate(row):
                cell_rect = pygame.Rect(col[0], col[1], CELL_SIZE, CELL_SIZE)
                if cell_rect.collidepoint(mouse_pos):
                    # Check if the coord was already shot
                    if self.match.shot_already_made(
                        {"x": col_idx, "y": row_idx}, player
                    ):
                        return None
                    return self.match.add_shot(player, {"x": col_idx, "y": row_idx})
        return None
