# Blokus AI

Blokus AI is a web-based implementation of the popular board game **Blokus**, enhanced with AI players. The game allows human players to compete against AI opponents using various algorithms, including **Greedy AI**, **Minimax AI**, and **Monte Carlo AI**.

## Features

- **Interactive Gameplay**: Play Blokus in your browser with a visually appealing interface.
- **AI Opponents**: Compete against AI players using different strategies:
  - **Greedy AI**: Chooses moves based on immediate utility.
  - **Minimax AI**: Uses a depth-limited minimax algorithm with alpha-beta pruning.
  - **Monte Carlo AI**: Simulates multiple games to find the best move.
- **Customizable Player Types**: Choose between human or AI players for each of the four players.
- **Real-Time Updates**: The game board and available pieces update dynamically.
- **Endgame Rankings**: Displays final rankings based on scores when the game ends.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [AI Algorithms](#ai-algorithms)
- [Project Structure](#project-structure)
- [Testing](#testing)

---

### Installation

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend development)
- Flask (backend framework)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blokus-ai.git
   cd blokus-ai
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
3. Navigate to the frontend directory and install the Node.js dependencies: 
    ```bash
    cd frontend
    npm install
4. Start the Flask backend:
    ```bash
    python app.py
5. Start the frontend development server:
    ```bash
    npm start

6. Open your browser and navigate to http://localhost:3000 to start playing Blokus AI.

### Game Rules

Blokus is a strategy board game where players take turns placing pieces on a 20x20 grid. The goal is to place as many of your pieces as possible while blocking your opponents. Pieces must touch at least one corner of your previously placed pieces but cannot share an edge.

### Testing
To run the backend tests, use the following command:
python3 -m unittest discover backend/tests

