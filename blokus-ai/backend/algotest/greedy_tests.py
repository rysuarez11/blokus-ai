import unittest
from backend.board import Board
from backend.piece import pieces
from backend.algorithms.greedy import GreedyAI

class TestGreedyAI(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
        self.pieces = [pieces['I5'], pieces['O4'], pieces['L4']]  # Test with a few pieces
        self.ai = GreedyAI(player_id=1, pieces=self.pieces)
        print("\n=== Starting New Test ===")
        print("Initial board state:")
        self.board.display_board()
        print("\n")

    def test_evaluate_move(self):
        print("\nTesting evaluate_move:")
        piece = pieces['O4']  # 2x2 square piece
        score = self.ai.calculate_utility(piece, 0, 0, self.board)  # Changed from evaluate_move
        print(f"Score for piece {piece.name} at (0,0): {score}")
        print("Board state after evaluation:")
        self.board.display_board()
        self.assertIsInstance(score, (int, float))
        self.assertTrue(score > float('-inf'))  # Changed condition since invalid moves return -inf

    def test_calculate_utility(self):
        print("\nTesting calculate_utility:")
        piece = pieces['O4']
        score = self.ai.calculate_utility(piece, 0, 0, self.board)
        print(f"Utility for piece {piece.name} at (0,0):")
        print(f"- Score: {score}")
        print(f"- Expected components:")
        print(f"  * Tile count: {sum(sum(piece.shape))}")
        print(f"  * Distance score: calculated from center")
        print(f"  * Blocking score: number of players blocked")
        self.assertIsInstance(score, (int, float))

    def test_choose_move_first_turn(self):
        print("\nTesting choose_move_first_turn:")
        move = self.ai.choose_move(self.board)
        print("\nBoard before move:")
        self.board.display_board()
        
        self.assertIsNotNone(move)
        if move:
            original_piece, oriented_piece, x, y = move
            print(f"\nChosen piece: {original_piece.name} at position ({x},{y})")
            print("Piece shape:")
            print(oriented_piece.shape)
            print(f"Utility score: {self.ai.calculate_utility(oriented_piece, x, y, self.board)}")
            
            print("\nBoard after move:")
            self.board.display_board()
            
            print("\nValidation result:", self.board.is_valid(oriented_piece, x, y, self.ai))
            self.assertTrue(self.board.is_valid(oriented_piece, x, y, self.ai))

    def test_blocking_score(self):
        print("\nTesting blocking score calculation:")
        # Place a piece on the board first
        piece = pieces['I5']
        self.board.place_piece(piece, 0, 0, self.ai)
        # Try to place another piece that would block moves
        blocking_piece = pieces['O4']
        score = self.ai.calculate_utility(blocking_piece, 1, 1, self.board)
        print(f"Blocking score for {blocking_piece.name} at (1,1): {score}")
        self.board.display_board()
        self.assertIsInstance(score, (int, float))

    def test_no_valid_moves(self):
        print("\nTesting no_valid_moves:")
        # Fill the board to leave no valid moves
        self.board.grid.fill(2)  # Fill with opponent's pieces
        print("Board state (filled with opponent pieces):")
        self.board.display_board()
        move = self.ai.choose_move(self.board)
        self.assertIsNone(move)

    def tearDown(self):
        print("\n=== Test Complete ===\n")

if __name__ == '__main__':
    unittest.main()
