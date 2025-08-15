import sys
import os

# Add the parent directory of 'backend' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.piece import pieces
from backend.player import Player
from backend.board import Board
from backend.piece import Piece

"""
TEST COMMAND
python3 backend/tests/orientations_test.py
"""

# # TESTS ALL POSSIBLE UNIQUE ORIENTATIONS
# def main():
#     player = Player(1, list(pieces.values()))
#     all_orientations = player.get_all_orientations()
#     for piece_name, orientations in all_orientations.items():
#         print(f"Piece: {piece_name}")
#         for i, orientation in enumerate(orientations):
#             print(f"Orientation {i + 1}:\n{orientation}\n")

# TESTS ALL POSSIBLE MOVES
def main():
    test_pieces_list = [
        # Piece([[1]], "I1"),
        # Piece([[1, 1]], "I2"),
        # Piece([[1, 1, 1]], "I3"),
        # Piece([[1, 1, 1, 1]], "I4"),
        Piece([[1, 1, 1], [0, 1, 0]], "T4")
    ]

    # Create a dictionary of test pieces for easy access
    test_pieces = {piece.name: piece for piece in test_pieces_list}

    board = Board()
    player = Player(1, list(test_pieces.values()))
    valid_moves = player.find_all_valid_moves(board)
    for move in valid_moves:
        piece, orientation, x, y = move
        print(f"Piece: {piece.name}, Orientation:\n{orientation}\nPosition: ({x}, {y})\n")

if __name__ == "__main__":
    main()