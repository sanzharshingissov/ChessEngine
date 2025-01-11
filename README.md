Chess Engine with AI

This project is a chess engine written in Python. It features a graphical user interface (GUI) for playing chess, 
the ability to play against another human or an AI opponent, 
and an implementation of basic chess rules and AI-driven move suggestions.

Features

Chess Rules Implementation:

Valid move generation.

Check, checkmate, and stalemate detection.

En passant, castling, and pawn promotion rules.

Graphical Interface:

Interactive chessboard built using Pygame.

Highlights valid moves and maintains a move log.

AI Opponent:

AI engine uses NegaMax and Alpha-Beta pruning to suggest optimal moves.

Configurable search depth for AI decision-making.

Random move generation for testing purposes.

Installation

Requirements

Python 3.6+

Pygame library

To install Pygame, run:

pip install pygame

Setup

Clone this repository:

git clone <https://github.com/sanzharshingissov/ChessEngine>

Place the images folder containing chess piece images in the root directory. The filenames should match the format wp.png, bp.png, wR.png, etc.

Usage

Run the main script to start the chess game:

python ChessMain.py

Game Modes

Player vs Player: Select human as the opponent.

Player vs AI: Select AI as the opponent.

Controls:

Mouse Input:

Click on a piece to select it.

Click on a destination square to move the piece.

Keyboard Shortcuts:

z: Undo the last move.

r: Reset the board.

File Overview:

ChessEngine.py

Handles game logic and the current state of the chessboard.

Validates moves and implements chess rules.

ChessMain.py

Main driver program for the GUI.

Manages user input and renders the game state.

SmartMoveFinder.py

Implements AI move calculation using:

Random move selection.

NegaMax algorithm with Alpha-Beta pruning.

AI Implementation:

The AI evaluates moves using the following techniques:

Material Score Evaluation:

Assigns point values to pieces:

Queen: 10

Rook: 5

Bishop/Knight: 3

Pawn: 1

Positive scores favor white, negative scores favor black.

NegaMax with Alpha-Beta Pruning:

Efficiently explores the game tree to a configurable depth (default: 4).

Prunes branches that cannot influence the outcome, speeding up calculations.

Future Improvements:

Add advanced chess features such as threefold repetition detection and fifty-move rule.

Improve AI by implementing a more sophisticated evaluation function.

Introduce a graphical interface for game mode selection.

Enable saving and loading of game states.

Contributing:

Contributions are welcome! Feel free to fork the repository and submit pull requests.

Acknowledgments:

Pygame Documentation for GUI development guidance.

Inspiration from various online resources.