
import numpy as np
from backend.move_validator import MoveValidator

class Board:

    def __init__(self, size=20):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.validator = MoveValidator(self.grid)

    def display_board(self):
        # Print boad
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def place_piece(self, piece, x, y, player):
        # Check valid placement
        if self.is_valid(piece, x, y, player):
            # Place piece (mark player_id)
            piece_height, piece_width = piece.shape.shape
            for i in range(piece_height):
                for j in range(piece_width):
                    if piece.shape[i, j] == 1:
                        self.grid[x + i, y + j] = player.player_id
            return True
        else:
            return False
        
    def is_valid(self, piece, x, y, player):
        # Validate placement coordinates
        return self.validator.within_bounds(piece, x, y) and \
               self.validator.not_overlapping(piece, x, y) and \
               (self.validator.touching_corner(piece, x, y, player) or self.validator.first_move(piece, x, y))
    
    def get_score(self):
        # Calculate the score for each player based on the number of tiles they have occupied
        scores = {1: 0, 2: 0, 3: 0, 4: 0}  # Initialize scores to zero for all players
        for row in self.grid:
            for cell in row:
                if cell != 0:  # If the cell is occupied by a player
                    scores[cell] += 1
        return scores
