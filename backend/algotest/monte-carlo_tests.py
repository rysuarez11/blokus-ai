import unittest
from backend.board import Board
from backend.piece import pieces
from backend.algorithms.monte_carlo import MonteCarloAI, Node

class TestMonteCarloAI(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
        self.pieces = [pieces['I5'], pieces['O4'], pieces['L4']]
        self.ai = MonteCarloAI(player_id=1, pieces=self.pieces, simulation_time=0.1)
        print("\n=== Starting New Test ===")
        print("Initial board state:")
        self.board.display_board()
        print("\n")

    def test_node_creation(self):
        print("\nTesting Node creation:")
        node = Node(self.board, self.ai)
        print("Node created with {0} untried moves".format(len(node.untried_moves)))
        self.assertIsInstance(node, Node)
        self.assertEqual(node.visits, 0)
        self.assertEqual(node.value, 0.0)

    def test_calculate_utility(self):
        print("\nTesting calculate_utility:")
        # Place a piece to test utility calculation
        piece = pieces['O4']
        self.board.place_piece(piece, 0, 0, self.ai)
        utility = self.ai.calculate_utility(self.board, self.ai.player_id)
        print("Utility score: {0}".format(utility))
        self.assertIsInstance(utility, float)
        self.board.display_board()

    def test_simulation(self):
        print("\nTesting simulation:")
        result = self.ai.simulate(self.board)
        print("Simulation result: {0}".format(result))
        self.assertIsInstance(result, float)

    def test_choose_move_first_turn(self):
        print("\nTesting choose_move_first_turn:")
        move = self.ai.choose_move(self.board)
        self.assertIsNotNone(move)
        if move:
            original_piece, oriented_piece, x, y = move
            print("\nChosen piece: {0} at position ({1},{2})".format(
                original_piece.name, x, y))
            print("Piece shape:")
            print(oriented_piece.shape)
            self.assertTrue(self.board.is_valid(oriented_piece, x, y, self.ai))

    def test_monte_carlo_search(self):
        print("\nTesting monte_carlo_search:")
        # Place initial piece to test non-first-turn scenario
        self.board.place_piece(pieces['O4'], 0, 0, self.ai)
        move = self.ai.monte_carlo_search(self.board)
        self.assertIsNotNone(move)
        if move:
            original_piece, oriented_piece, x, y = move
            print("Monte Carlo search chose: {0} at ({1},{2})".format(
                original_piece.name, x, y))
            self.assertTrue(self.board.is_valid(oriented_piece, x, y, self.ai))

    def test_no_valid_moves(self):
        print("\nTesting no_valid_moves:")
        self.board.grid.fill(2)  # Fill with opponent's pieces
        print("Board state (filled with opponent pieces):")
        self.board.display_board()
        move = self.ai.choose_move(self.board)
        self.assertIsNone(move)

    def tearDown(self):
        print("\n=== Test Complete ===\n")

if __name__ == '__main__':
    unittest.main()
