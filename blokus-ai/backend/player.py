from backend.piece import Piece
from copy import deepcopy

class Player:
    def __init__(self, player_id, pieces):
        self.player_id = player_id
        self.pieces = pieces

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def choose_move(self, board):
        print(f"Player {self.player_id}, choose a move.")
        
        for i, piece in enumerate(self.pieces):
            print(f"{i}: \n{piece.shape}\n")

        piece_index = int(input("Select a piece by index: "))
        if piece_index < 0 or piece_index >= len(self.pieces):
            print("Invalid selection")
            return None
        
        original_piece = self.pieces[piece_index]
        piece = deepcopy(original_piece)

        # Ask if the player wants to rotate or flip the piece
        while True:
            transform = input("Enter transformations (r for rotate, f for flip, done to finish): ").strip().lower()
            if transform == 'r':
                piece.rotate()
            elif transform == 'f':
                piece.flip()
            elif transform == 'done':
                break
            else:
                print("Invalid input. Enter 'r' to rotate, 'f' to flip, or 'done' to finish.")

        x = int(input("Enter row coordinate: "))
        y = int(input("Enter column coordinate: "))
    
        if board.is_valid(piece, x, y, self):
            return original_piece, piece, x, y
        else:
            print("Invalid move. Try again.")
            return None
        
    def get_all_orientations(self):
        all_orientations = {}
        for piece in self.pieces:
            all_orientations[piece.name] = piece.all_orientations()
        return all_orientations

    def find_all_valid_moves(self, board):
        valid_moves = []
        for piece in self.pieces:
            for orientation in piece.all_orientations():
                orientation_piece = Piece(orientation, piece.name)  # Create a Piece object for each orientation
                for x in range(board.size):
                    for y in range(board.size):
                        if board.is_valid(orientation_piece, x, y, self):
                            valid_moves.append((piece, orientation_piece, x, y))
        print(f"🔍 Player {self.player_id} valid moves: {len(valid_moves)}")
        return valid_moves