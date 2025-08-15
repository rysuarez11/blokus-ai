from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np
from copy import deepcopy

def debug_print(message, piece=None, x=None, y=None, validation=None):
    """Debug print function for minimax algorithm"""
    print("\nDEBUG:", message)
    if piece is not None and hasattr(piece, 'name'):
        print(f"Piece: {piece.name}")
        print("Shape:\n", piece.shape)
    if x is not None and y is not None:
        print(f"Position: ({x}, {y})")
    if validation is not None:
        print(f"Additional info: {validation}")
    print("-" * 50)

class MinimaxAI(Player):
    def __init__(self, player_id, pieces, max_depth=3):
        super().__init__(player_id, pieces)
        self.max_depth = max_depth
        self.board_center = 10

    def count_valid_corners(self, piece, x, y, board):
        """Count number of valid corners created by placing this piece"""
        test_board = Board(board.size)
        test_board.grid = np.copy(board.grid)
        test_board.place_piece(piece, x, y, self)
        
        valid_corners = set()
        height, width = piece.shape.shape
        
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    diagonals = [
                        (x + i + 1, y + j + 1),
                        (x + i + 1, y + j - 1),
                        (x + i - 1, y + j + 1),
                        (x + i - 1, y + j - 1)
                    ]
                    
                    for dx, dy in diagonals:
                        if not (0 <= dx < board.size and 0 <= dy < board.size):
                            continue
                        if (dx, dy) in valid_corners:
                            continue
                        if test_board.grid[dx, dy] != 0:
                            continue
                            
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
        """Calculate utility score based on tiles, distance, and corners"""
        # Base score from number of tiles
        tile_count = int(np.sum(piece.shape))
        
        # Calculate distance from closest tile to center
        min_distance = float('inf')
        height, width = piece.shape.shape
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    tile_x, tile_y = x + i, y + j
                    distance = (abs(tile_x - self.board_center) + 
                              abs(tile_y - self.board_center))
                    min_distance = min(min_distance, distance)
        
        # Count valid corners for future moves
        corner_count = self.count_valid_corners(piece, x, y, board)
        
        return float(tile_count - min_distance + corner_count)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0:
            return None, self.evaluate_board(board)
                
        valid_moves = self.find_all_valid_moves(board)
        if not valid_moves:
            return None, float('-inf')
        
        # Calculate utility for all moves and sort by utility
        moves_with_utility = [
            (piece, oriented_piece, x, y, self.calculate_utility(oriented_piece, x, y, board))
            for piece, oriented_piece, x, y in valid_moves
        ]
        moves_with_utility.sort(key=lambda x: x[4], reverse=True)
        
        # Take top 10 moves after sorting by utility
        valid_moves = [(m[0], m[1], m[2], m[3]) for m in moves_with_utility[:10]]

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for piece, oriented_piece, x, y in valid_moves[:10]:
                # Calculate immediate utility of this move
                immediate_utility = self.calculate_utility(oriented_piece, x, y, board)
                
                # Create new board with this move
                board_copy = Board(board.size)
                board_copy.grid = np.copy(board.grid)
                board_copy.place_piece(oriented_piece, x, y, self)
                
                # Combine immediate utility with future evaluation
                _, future_eval = self.minimax(board_copy, depth - 1, alpha, beta, False)
                eval_score = immediate_utility + future_eval
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (piece, oriented_piece, x, y)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for piece, oriented_piece, x, y in valid_moves[:10]:
                # Calculate immediate utility of this move
                immediate_utility = self.calculate_utility(oriented_piece, x, y, board)
                
                board_copy = Board(board.size)
                board_copy.grid = np.copy(board.grid)
                board_copy.place_piece(oriented_piece, x, y, self)
                
                # Combine immediate utility with future evaluation
                _, future_eval = self.minimax(board_copy, depth - 1, alpha, beta, True)
                eval_score = immediate_utility + future_eval
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (piece, oriented_piece, x, y)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return best_move, min_eval
        
    def evaluate_board(self, board):
        """Evaluate the current board state"""
        # Count my pieces vs opponent pieces
        my_pieces = np.sum(board.grid == self.player_id)
        opponent_pieces = np.sum(board.grid != 0) - my_pieces
        
        # Look for valid moves I have
        valid_moves = len(self.find_all_valid_moves(board))
        
        # Combined score favoring more pieces and more available moves
        return float(my_pieces - opponent_pieces + (0.5 * valid_moves))

    def choose_move(self, board):
        """Choose best move using minimax"""
        debug_print("Starting minimax search")
        
        # Use minimax for all other moves
        best_move, _ = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)
        if best_move:
            debug_print("Selected move", best_move[1], best_move[2], best_move[3])
        return best_move