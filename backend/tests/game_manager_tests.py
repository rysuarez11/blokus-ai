import unittest
from unittest.mock import patch
import builtins
from copy import deepcopy
from backend.piece import Piece, pieces
from backend.player import Player
from backend.board import Board
from backend.game_manager import GameManager

"""
TEST COMMAND
python3 -m unittest backend.tests.game_manager_tests
"""

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.pieces = [
            deepcopy(pieces["V3"]),
            deepcopy(pieces["O4"]),
            deepcopy(pieces["L4"])
        ]
        self.player1 = Player(1, deepcopy(self.pieces))
        self.player2 = Player(2, deepcopy(self.pieces))
        self.player3 = Player(3, deepcopy(self.pieces))
        self.player4 = Player(4, deepcopy(self.pieces))
        self.game_manager = GameManager(self.player1, self.player2, self.player3, self.player4)

    def test_init(self):
        self.assertEqual(len(self.game_manager.players), 4)
        self.assertEqual(self.game_manager.current_turn, 0)
        self.assertIsInstance(self.game_manager.board, Board)
        self.assertFalse(self.game_manager.game_over)

    def test_next_turn(self):
        self.game_manager.next_turn()
        self.assertEqual(self.game_manager.current_turn, 1)
        self.game_manager.next_turn()
        self.assertEqual(self.game_manager.current_turn, 2)
        self.game_manager.next_turn()
        self.assertEqual(self.game_manager.current_turn, 3)
        self.game_manager.next_turn()
        self.assertEqual(self.game_manager.current_turn, 0)

    # @patch('builtins.input', side_effect=['0', 'done', '0', '0'])
    # def test_play_turn_valid_move(self, mock_input):
    #     self.assertEqual(self.game_manager.current_turn, 0)
    #     self.game_manager.play_turn()
    #     self.assertEqual(self.game_manager.current_turn, 1)
    #     self.assertNotIn(self.pieces[0], self.player1.pieces)

    # @patch('builtins.input', side_effect=['0', 'done', '0', '0'])
    # def test_play_game(self, mock_input):
    #     with patch.object(self.game_manager, 'check_game_over', return_value=True):
    #         self.game_manager.play_game()
    #         self.assertTrue(self.game_manager.game_over)
