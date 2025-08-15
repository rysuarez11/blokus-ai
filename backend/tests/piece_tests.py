import unittest
import numpy as np
from copy import deepcopy
from backend.piece import Piece, pieces

"""
TEST COMMAND
python3 -m unittest backend.tests.piece_tests
"""

class TestPiece(unittest.TestCase):
    def setUp(self):
        self.piece = deepcopy(pieces["V3"])  # Use the V3 from the pieces list

    def test_rotate(self):
        self.piece.rotate()
        expected_shape = np.array([[1, 0], [1, 1]])  # Expected shape after rotation
        self.assertTrue((self.piece.shape == expected_shape).all())

    def test_flip(self):
        self.piece.flip()
        expected_shape = np.array([[1, 1], [0, 1]])  # Expected shape after flip
        self.assertTrue((self.piece.shape == expected_shape).all())

    def test_repr(self):
        expected_repr = "V3: \n[[1 1]\n [1 0]]"
        self.assertEqual(repr(self.piece), expected_repr)

if __name__ == "__main__":
    unittest.main()