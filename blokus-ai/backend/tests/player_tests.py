import unittest
import builtins
import numpy as np
from backend.player import Player
from backend.piece import Piece
from backend.board import Board

"""
TEST COMMAND
python3 -m unittest backend.tests.player_tests
"""

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.pieces = [
            Piece([[1, 1], [1, 1]], "O4"),
            Piece([[1, 0], [1, 1]], "L3")
        ]
        self.player = Player(1, self.pieces)
        self.board = Board()

    def test_init(self):
        # Test initialization
        self.assertEqual(self.player.player_id, 1)
        self.assertEqual(self.player.pieces, self.pieces)

    def test_remove_piece(self):
        # Test removing a piece
        piece_to_remove = self.pieces[0]
        self.player.remove_piece(piece_to_remove)
        self.assertNotIn(piece_to_remove, self.player.pieces)

    # def test_choose_move_valid(self):
    #     # Simulate user input for a valid move
    #     inputs = iter(['0', 'done', '0', '0'])
    #     def mock_input(prompt):
    #         return next(inputs)
        
    #     original_input = builtins.input
    #     builtins.input = mock_input
    #     try:
    #         piece, x, y = self.player.choose_move(self.board)
    #         self.assertEqual(piece, self.pieces[0])
    #         self.assertEqual(x, 0)
    #         self.assertEqual(y, 0)
    #     finally:
    #         builtins.input = original_input

    # def test_choose_move_invalid_selection(self):
    #     # Simulate user input for an invalid piece index
    #     inputs = iter(['2', '0', '0'])
    #     def mock_input(prompt):
    #         return next(inputs)
        
    #     original_input = builtins.input
    #     builtins.input = mock_input
    #     try:
    #         result = self.player.choose_move(self.board)
    #         self.assertIsNone(result)
    #     finally:
    #         builtins.input = original_input

    # def test_choose_move_invalid_move(self):
    #     # Simulate user input for an invalid move
    #     inputs = iter(['0', '11', '8'])
    #     def mock_input(prompt):
    #         return next(inputs)
        
    #     original_input = builtins.input
    #     builtins.input = mock_input
    #     try:
    #         result = self.player.choose_move(self.board)
    #         self.assertIsNone(result)
    #     finally:
    #         builtins.input = original_input


if __name__ == "__main__":
    unittest.main()