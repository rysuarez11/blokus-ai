from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np
from copy import deepcopy
import random
import math
import time

class Node:
    def __init__(self, board, player, move=None, parent=None):
        self.board = board
        self.player = player
        self.move = move  # (original_piece, oriented_piece, x, y)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_moves = player.find_all_valid_moves(board)
        random.shuffle(self.untried_moves)  # Randomize move exploration

    def add_child(self, move, board, player):
        child = Node(board, player, move, self)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.value += result

    def fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.414):
        if not self.children:
            return None
        choices = [(child.value / child.visits) + c_param * 
                  math.sqrt(2 * math.log(self.visits) / child.visits)
                  for child in self.children]
        return self.children[choices.index(max(choices))]

class MonteCarloAI(Player):
    def __init__(self, player_id, pieces, simulation_time=30):
        super().__init__(player_id, pieces)
        self.simulation_time = simulation_time
        self.board_center = (9.5, 9.5)  # Match GreedyAI's board center

    def count_valid_corners(self, piece, x, y, board):
        """Same corner counting logic as GreedyAI"""
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
        """Same utility calculation as GreedyAI"""
        # Base score from number of tiles
        tile_count = int(np.sum(piece.shape))
        
        # Calculate distance from closest tile to center
        min_distance = float('inf')
        height, width = piece.shape.shape
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    tile_x, tile_y = x + i, y + j
                    distance = (abs(tile_x - self.board_center[0]) + 
                              abs(tile_y - self.board_center[1]))
                    min_distance = min(min_distance, distance)
        
        # Count valid corners for future moves
        corner_count = self.count_valid_corners(piece, x, y, board)
        
        return float(tile_count - min_distance + (0.5 * corner_count))

    def choose_move(self, board):
        return self.monte_carlo_search(board)

    def monte_carlo_search(self, board):
        root = Node(board, self)
        
        # Ensure we expand at least one child
        if not root.untried_moves:
            return None
            
        # Run MCTS for given time
        end_time = time.time() + self.simulation_time
        while time.time() < end_time:
            node = root
            board_copy = deepcopy(board)
            
            # Selection and Expansion
            while node.untried_moves == [] and node.children != []:
                node = node.best_child()
                if node.move:
                    board_copy.place_piece(node.move[1], node.move[2], node.move[3], self)
            
            # Expand
            if node.untried_moves:
                move = node.untried_moves[0]  # Take first untried move
                board_copy.place_piece(move[1], move[2], move[3], self)
                node = node.add_child(move, board_copy, self)
                
            # Simulation and Backpropagation
            score = self.simulate(board_copy)
            while node is not None:
                node.update(score)
                node = node.parent
                
        # Choose best move
        best_child = root.best_child(c_param=0.0)
        if best_child and best_child.move:
            return best_child.move
            
        # If no moves found, return None
        return None

    def simulate(self, board):
            simulation_board = deepcopy(board)
            current_player = self
            moves_count = 0
            max_moves = 3  # Increased depth
            total_utility = 0

            while moves_count < max_moves:
                valid_moves = current_player.find_all_valid_moves(simulation_board)
                if not valid_moves:
                    break

                # Sort moves by utility and choose from top moves
                moves_with_utility = [
                    (move, self.calculate_utility(move[1], move[2], move[3], simulation_board))
                    for move in valid_moves
                ]
                moves_with_utility.sort(key=lambda x: x[1], reverse=True)
                top_moves = moves_with_utility[:10]  # Consider only top 5 moves
                
                # Choose randomly from top moves
                move, utility = random.choice(top_moves)
                total_utility += utility
                
                simulation_board.place_piece(move[1], move[2], move[3], current_player)
                moves_count += 1

            return total_utility