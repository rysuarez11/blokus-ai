from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np
import random

def debug_print(message, piece=None, x=None, y=None, validation=None):
    print("\nDEBUG:", message)
    if piece is not None:
        print(f"Piece: {piece.name}")
        print("Shape:\n", piece.shape)
    if x is not None and y is not None:
        print(f"Position: ({x}, {y})")
    if validation is not None:
        print(f"Validation result: {validation}")
    print("-" * 50)

class GreedyAI(Player):
    def __init__(self, player_id, pieces):
        super().__init__(player_id, pieces)
        self.board_center = (9.5, 9.5)  # For a 19x19 board

    def count_valid_corners(self, piece, x, y, board):
        """Count valid corners for future moves after placing this piece"""
        # Create a board copy with the piece placed
        test_board = Board(board.size)
        test_board.grid = np.copy(board.grid)
        test_board.place_piece(piece, x, y, self)
        
        # Keep track of unique corner positions
        valid_corners = set()
        height, width = piece.shape.shape
        
        # Check each tile of the piece
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    # Check all diagonal positions around this tile
                    diagonals = [
                        (x + i + 1, y + j + 1),
                        (x + i + 1, y + j - 1),
                        (x + i - 1, y + j + 1),
                        (x + i - 1, y + j - 1)
                    ]
                    
                    for dx, dy in diagonals:
                        # Skip if outside board or already counted
                        if not (0 <= dx < board.size and 0 <= dy < board.size):
                            continue
                        if (dx, dy) in valid_corners:
                            continue
                        
                        # Corner must be empty
                        if test_board.grid[dx, dy] != 0:
                            continue
                        
                        # Check orthogonal adjacency (must not touch any same player pieces)
                        valid = True
                        for adj_x, adj_y in [(dx-1, dy), (dx+1, dy), (dx, dy-1), (dx, dy+1)]:
                            if (0 <= adj_x < board.size and 0 <= adj_y < board.size):
                                if test_board.grid[adj_x, adj_y] == self.player_id:
                                    valid = False
                                    break
                        
                        if valid:
                            valid_corners.add((dx, dy))
        
        return len(valid_corners)

    def calculate_utility(self, piece, x, y, board):
        """Calculate utility score based on:
        1. Number of tiles in piece
        2. Distance to center
        3. Number of valid corners created"""
        
        # Base score from number of tiles
        tile_count = int(np.sum(piece.shape))
        
        # Calculate distance from closest tile to center
        min_distance = float('inf')
        height, width = piece.shape.shape
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    tile_x, tile_y = x + i, y + j
                    distance = (abs(tile_x - self.board_center[0]) + 
                            abs(tile_y - self.board_center[1]))
                    min_distance = min(min_distance, distance)
        
        # Count valid corners for future moves
        corner_count = self.count_valid_corners(piece, x, y, board)
        
        # Debug output
        debug_print(f"Move evaluation", piece, x, y,
                    f"Tiles: {tile_count}, Distance: {min_distance}, Corners: {corner_count}")
        
        # Weight the components
        return float(tile_count - min_distance + (0.5 * corner_count))

    def choose_move(self, board):
        debug_print("Starting choose_move")
            
        valid_moves = self.find_all_valid_moves(board)
        
        # Find best move
        best_score = float('-inf')
        best_move = None
        
        for piece, oriented_piece, x, y in valid_moves:
            utility = self.calculate_utility(oriented_piece, x, y, board)
            debug_print(f"Evaluating move", oriented_piece, x, y, f"Score: {utility}")
            
            if utility > best_score:
                best_score = utility
                best_move = (piece, oriented_piece, x, y)
                debug_print("New best move found")
        
        if best_move:
            debug_print("Selected best move", best_move[1], best_move[2], best_move[3])
            return best_move
            
        return None