import numpy as np

class MoveValidator:
    def __init__(self, grid):
        self.grid = grid

    def within_bounds(self, piece, x, y):
        # Check bounds
        piece_height, piece_width = piece.shape.shape
        return 0 <= x <= self.grid.shape[0] - piece_height and 0 <= y <= self.grid.shape[1] - piece_width

    def not_overlapping(self, piece, x, y):
        # Check overlap
        piece_height, piece_width = piece.shape.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    if self.grid[x + i, y + j] != 0:  # If the cell is not empty
                        return False
        return True
    
    def first_move(self, piece, x, y):
        # Check if the piece is placed at one of the corner coordinates
        piece_height, piece_width = piece.shape.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:
                    if (x + i == 0 and y + j == 0) or \
                       (x + i == 0 and y + j == self.grid.shape[1] - 1) or \
                       (x + i == self.grid.shape[0] - 1 and y + j == 0) or \
                       (x + i == self.grid.shape[0] - 1 and y + j == self.grid.shape[1] - 1):
                        return True
        return False
    
    def touching_corner(self, piece, x, y, player):
        # Check if the piece only touches the corners of other pieces
        piece_height, piece_width = piece.shape.shape
        touching_corner = False
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    # Check adjacent cells to ensure no edge sharing
                    if (x + i > 0 and self.grid[x + i - 1, y + j] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and self.grid[x + i + 1, y + j] == player.player_id) or \
                       (y + j > 0 and self.grid[x + i, y + j - 1] == player.player_id) or \
                       (y + j < self.grid.shape[1] - 1 and self.grid[x + i, y + j + 1] == player.player_id):
                        return False
                    # Check diagonal cells to ensure corner touching
                if piece.shape[i, j] == 1:
                    if (x + i > 0 and y + j > 0 and self.grid[x + i - 1, y + j - 1] == player.player_id) or \
                       (x + i > 0 and y + j < self.grid.shape[1] - 1 and self.grid[x + i - 1, y + j + 1] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and y + j > 0 and self.grid[x + i + 1, y + j - 1] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and y + j < self.grid.shape[1] - 1 and self.grid[x + i + 1, y + j + 1] == player.player_id):
                                touching_corner = True
        return touching_corner