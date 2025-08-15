from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from backend.board import Board
from backend.piece import pieces, Piece
from backend.player import Player
from backend.move_validator import MoveValidator

from backend.algorithms.greedy import GreedyAI
from backend.algorithms.minimax import MinimaxAI
from backend.algorithms.monte_carlo import MonteCarloAI

app = Flask(__name__)
CORS(app)

# Initialize players and board
players = {i: Player(i, list(pieces.values())) for i in range(1, 5)}
board = Board(size=20)
board.current_player = 1

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({'board': board.grid.tolist(), 'current_player': board.current_player})

@app.route('/get_pieces', methods=['GET'])
def get_pieces():
    current_player = board.current_player
    current_player_pieces = players[current_player].pieces

    pieces_data = [{"name": piece.name, "shape": piece.shape.tolist()} for piece in current_player_pieces]
    return jsonify({"pieces": pieces_data})

@app.route('/rotate_piece_hover', methods=['POST'])
def rotate_piece_hover():
    """Rotate a piece on hover and return new shape."""
    data = request.json
    piece_name = data.get("piece")

    for player in players.values():
        for piece in player.pieces:
            if piece.name == piece_name:
                piece.rotate()
                return jsonify({"shape": piece.shape.tolist()})

    return jsonify({"error": "Piece not found"}), 404

@app.route('/rotate_piece_keypress', methods=['POST'])
def rotate_piece_keypress():
    """Rotate or flip a piece when 'r' or 'f' is pressed."""
    data = request.json
    piece_name = data.get("piece")
    action = data.get("action")  # "rotate" or "flip"

    for player in players.values():
        for piece in player.pieces:
            if piece.name == piece_name:
                if action == "rotate":
                    piece.rotate()
                elif action == "flip":
                    piece.flip()
                return jsonify({"shape": piece.shape.tolist()})

    return jsonify({"error": "Piece not found"}), 404
    
@app.route("/place_piece", methods=["POST"])
def place_piece():
    """Attempt to place a piece on the board."""
    data = request.json
    piece_name = data.get("piece")
    piece_shape_list = data.get("shape")
    x, y = data.get("x"), data.get("y")
    current_player = board.current_player

    piece_shape = np.array(piece_shape_list)

    selected_piece = next((p for p in players[current_player].pieces if p.name == piece_name), None)

    if selected_piece is None:
        print(f"❌ DEBUG: Piece {piece_name} not found in Player {current_player}'s inventory!")
        return jsonify({"success": False, "error": "Piece not found"}), 400

    if not board.place_piece(selected_piece, x, y, players[current_player]):
        return jsonify({"success": False, "error": "Invalid move."}), 400

    # call `remove_piece()`
    players[current_player].remove_piece(selected_piece)  

    next_player = (current_player % 4) + 1
    board.current_player = next_player  

    return jsonify({
        "success": True,
        "board": board.grid.tolist(),
        "next_player": next_player,
        "pieces": [{"name": piece.name, "shape": piece.shape.tolist()} for piece in players[next_player].pieces]
    })

@app.route('/end_turn', methods=['POST'])
def end_turn():
    current_player = board.current_player
    next_player = (current_player % 4) + 1

    # Skip players with no valid moves
    while not players[next_player].find_all_valid_moves(board):
        print(f"🚫 Player {next_player} has no valid moves. Skipping turn...")
        next_player = (next_player % 4) + 1
        if next_player == current_player:
            # All players have no valid moves, end the game
            print("🏁 All players have no valid moves. Ending the game...")
            scores = board.get_score()
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            rankings = [{"player_id": player_id, "score": score} for player_id, score in sorted_scores]
            return jsonify({
                "success": True,
                "game_over": True,
                "rankings": rankings
            })

    board.current_player = next_player
    print(f"➡️ Next turn: Player {next_player}")
    return jsonify({
        "success": True,
        "game_over": False,
        "next_player": next_player,
        "board": board.grid.tolist(),
        "pieces": [{"name": piece.name, "shape": piece.shape.tolist()} for piece in players[next_player].pieces]
    })

@app.route('/initialize_players', methods=['POST'])
def initialize_players():
    """Initialize player types (human or AI)."""
    data = request.json
    player_types = data.get("player_types")  # Example: ["greedy", "human", "human", "human"]

    print("🔍 Initializing players with types:", player_types)

    global players
    players = {}
    for i, player_type in enumerate(player_types, start=1):
        if player_type == "human":
            players[i] = Player(i, list(pieces.values()))
        elif player_type == "greedy":
            players[i] = GreedyAI(i, list(pieces.values()))
        elif player_type == "minimax":
            players[i] = MinimaxAI(i, list(pieces.values()))
        elif player_type == "monte_carlo":
            players[i] = MonteCarloAI(i, list(pieces.values()))
        print(f"✅ Player {i} initialized as {player_type}")
    return jsonify({"success": True})

@app.route('/process_ai_move', methods=['POST'])
def process_ai_move():
    """Process AI move and return the updated board."""
    current_player = board.current_player
    player = players[current_player]

    print(f"🔍 Processing move for Player {current_player} ({type(player).__name__})")

    # Check if the current player is an AI
    if isinstance(player, (GreedyAI, MinimaxAI, MonteCarloAI)):
        move = player.choose_move(board)
        if move:
            original_piece, piece, x, y = move
            print(f"✅ AI chose move: {piece.name} at ({x}, {y})")
            board.place_piece(piece, x, y, player)
            players[current_player].remove_piece(original_piece)
        else:
            print(f"❌ No valid moves for Player {current_player}. Skipping turn.")

        # Move to the next player
        next_player = (current_player % 4) + 1
        while not players[next_player].find_all_valid_moves(board):
            next_player = (next_player % 4) + 1
            if next_player == current_player:
                # All players have no valid moves, end the game
                scores = board.get_score()
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                rankings = [{"player_id": player_id, "score": score} for player_id, score in sorted_scores]
                return jsonify({
                    "success": True,
                    "game_over": True,
                    "rankings": rankings
                })

        board.current_player = next_player
        return jsonify({
            "success": True,
            "game_over": False,
            "board": board.grid.tolist(),
            "next_player": next_player,
            "pieces": [{"name": piece.name, "shape": piece.shape.tolist()} for piece in players[next_player].pieces]
        })

    print(f"❌ Player {current_player} is not an AI.")
    return jsonify({"success": False, "error": "No valid moves or invalid player type."}), 400

@app.route('/restart_game', methods=['POST'])
def restart_game():
    """Restart the game by resetting the board and players."""
    global players, board
    players = {i: Player(i, list(pieces.values())) for i in range(1, 5)}
    board = Board(size=20)
    board.current_player = 1
    print("🔄 Game has been restarted.")
    return jsonify({"success": True, "board": board.grid.tolist()})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
