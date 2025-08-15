import numpy as np
from copy import deepcopy

class Piece:

    def __init__(self, shape, name):
        self.shape = np.array(shape)
        self.name = name

    def rotate(self):
        self.shape = np.rot90(self.shape)

    def flip(self):
        self.shape = np.fliplr(self.shape)

    def all_orientations(self):
        orientations = []
        piece_copy = deepcopy(self)
        for _ in range(4):
            piece_copy.rotate()
            if not any(np.array_equal(piece_copy.shape, orientation) for orientation in orientations):
                orientations.append(piece_copy.shape.copy())
            piece_copy.flip()
            if not any(np.array_equal(piece_copy.shape, orientation) for orientation in orientations):
                orientations.append(piece_copy.shape.copy())
            piece_copy.flip()  # Flip back to original orientation before next rotation
        return orientations

    def __repr__(self):
        return f"{self.name}: \n{self.shape}"

# Define all 21 Blokus pieces
pieces_list = [
    Piece([[1]], "I1"),
    Piece([[1, 1]], "I2"),
    Piece([[1, 1, 1]], "I3"),
    Piece([[1, 1, 1, 1]], "I4"),
    Piece([[1, 1, 1, 1, 1]], "I5"),
    Piece([[1, 1], [1, 0]], "V3"),
    Piece([[1, 1, 0], [0, 1, 1]], "Z4"),
    Piece([[1, 1, 1], [0, 1, 0]], "T4"),
    Piece([[1, 1, 1], [1, 0, 0]], "L4"),
    Piece([[1, 1], [1, 1]], "O4"),
    Piece([[0, 1, 1], [1, 1, 0], [0, 1, 0]], "F5"),
    Piece([[1, 1, 1], [0, 1, 0], [0, 1, 0]], "T5"),
    Piece([[1, 1], [1, 1], [1, 0]], "P5"),
    Piece([[1, 0, 0], [1, 1, 0], [0, 1, 1]], "W5"),
    Piece([[0, 1, 0], [1, 1, 1], [0, 1, 0]], "X5"),
    Piece([[1, 1, 0], [0, 1, 0], [0, 1, 1]], "Z5"),
    Piece([[1, 0, 0], [1, 0, 0], [1, 1, 1]], "V5"),
    Piece([[1, 0, 1], [1, 1, 1]], "U5"),
    Piece([[1, 1, 1, 0], [0, 0, 1, 1]], "N5"),
    Piece([[1, 1, 1, 1], [0, 1, 0, 0]], "Y5"),
    Piece([[1, 1, 1, 1], [1, 0, 0, 0]], "L5")
]

# Create a dictionary to map piece names to Piece objects
pieces = {piece.name: piece for piece in pieces_list}