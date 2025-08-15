import unittest
import numpy as np
from backend.move_validator import MoveValidator
from backend.piece import Piece

"""
TEST COMMAND
python3 -m unittest backend.tests.move_validator_tests
"""

class MockPiece:
    def __init__(self, shape):
        self.shape = np.array(shape)

class MockPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

class TestMoveValidator(unittest.TestCase):
    def setUp(self):
        self.grid = np.zeros((20, 20), dtype=int)
        self.validator = MoveValidator(self.grid)
        self.player1 = MockPlayer(1)
        self.player2 = MockPlayer(2)

    def test_within_bounds(self):
        # Test within bounds
        piece = Piece([[1, 1], [1, 1]], "O4")
        self.assertTrue(self.validator.within_bounds(piece, 0, 0))
        self.assertFalse(self.validator.within_bounds(piece, 19, 19))

    def test_not_overlapping(self):
        # Test not overlapping
        piece = Piece([[1, 1], [1, 1]], "O4")
        self.grid[0, 0] = 1
        self.assertFalse(self.validator.not_overlapping(piece, 0, 0))
        self.assertTrue(self.validator.not_overlapping(piece, 1, 1))

    def test_touching_corner(self):
        # Test touching corner
        piece = Piece([[1, 1], [1, 1]], "O4")
        self.grid[1, 1] = 1
        self.assertFalse(self.validator.touching_corner(piece, 0, 0, self.player1))  # Overlapping, should be False
        self.assertFalse(self.validator.touching_corner(piece, 0, 2, self.player1))   # Touching edge, should be false
        self.assertFalse(self.validator.touching_corner(piece, 2, 0, self.player1))   # Touching edge, should be false
        self.assertTrue(self.validator.touching_corner(piece, 2, 2, self.player1))  # Not touching, should be True
        self.assertFalse(self.validator.touching_corner(piece, 2, 2, self.player2))  # Wrong player, should be False