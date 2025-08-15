import unittest
import numpy as np
from backend.board import Board
from backend.piece import Piece
from backend.move_validator import MoveValidator

"""
TEST COMMAND
python3 -m unittest backend.tests.board_tests
"""

class MockPiece:
    def __init__(self, shape):
        self.shape = np.array(shape)

class MockPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = MockPlayer(1)
        self.player2 = MockPlayer(2)

    def test_initial_board(self):
        # Test initial board state
        expected_grid = np.zeros((20, 20), dtype=int)
        np.testing.assert_array_equal(self.board.grid, expected_grid)

    def test_within_bounds(self):
        # Test within bounds
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.assertTrue(self.board.validator.within_bounds(piece, 0, 0))
        self.assertFalse(self.board.validator.within_bounds(piece, 19, 19))

    def test_not_overlapping(self):
        # Test not overlapping
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.board.grid[0, 0] = 1
        self.assertFalse(self.board.validator.not_overlapping(piece, 0, 0))
        self.assertTrue(self.board.validator.not_overlapping(piece, 1, 1))

    def test_touching_corner(self):
        # Test touching corner
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.board.grid[1, 1] = 1
        self.assertFalse(self.board.validator.touching_corner(piece, 0, 0, self.player1))
        self.assertTrue(self.board.validator.touching_corner(piece, 2, 2, self.player1))

    def test_first_move(self):
        # Test touching corner
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.assertFalse(self.board.validator.first_move(piece, 1, 1))
        self.assertTrue(self.board.validator.first_move(piece, 0, 0))

    def test_is_valid(self):
        # Test is valid
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.assertTrue(self.board.is_valid(piece, 0, 0, self.player1))

    def test_place_piece(self):
        # Test place piece
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.assertTrue(self.board.place_piece(piece, 0, 0, self.player1))

    def test_display_board(self):
        # Test display board
        piece = Piece([[1, 1], [1, 0]], "V3")
        self.board.place_piece(piece, 0, 0, self.player2)
        self.board.place_piece(piece, 18, 0, self.player2)
        self.board.place_piece(piece, 16, 2, self.player2)
        self.board.place_piece(piece, 14, 4, self.player2)
        self.board.display_board()

    def test_get_score(self):
        # Test with an empty board
        self.assertEqual(self.board.get_score(), {1: 0, 2: 0, 3: 0, 4: 0})

        # Test with one piece placed by player 1
        piece1 = Piece([[1, 1], [1, 0]], "V3")
        self.board.place_piece(piece1, 0, 0, self.player1)
        self.assertEqual(self.board.get_score(), {1: 3, 2: 0, 3: 0, 4: 0})

        # Test with one piece placed by player 2
        piece2 = Piece([[1, 1], [1, 0]], "V3")
        self.board.place_piece(piece2, 0, 18, self.player2)
        self.assertEqual(self.board.get_score(), {1: 3, 2: 3, 3: 0, 4: 0})

        # Test with one piece placed by player 2
        piece3 = Piece([[1, 1, 1]], "I3")
        self.board.place_piece(piece3, 1, 2, self.player1)
        self.assertEqual(self.board.get_score(), {1: 6, 2: 3, 3: 0, 4: 0})

if __name__ == "__main__":
    unittest.main()