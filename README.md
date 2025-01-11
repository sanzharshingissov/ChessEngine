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

Sanzhar Shingissov. Mtrc number: 66683228

In this project, I implemented several key features, including castling, en passant, and pawn promotion mechanics.
I also developed the move animation system and added functionality for highlighting valid moves on the chessboard. 
The most challenging aspect for me was implementing the AI using the NegaMax algorithm with Alpha-Beta pruning, as it required a deep understanding of game trees and optimization techniques. 
Through this work, I learned about the intricacies of chess rules, algorithmic thinking, and efficient coding practices.
This experience significantly improved my problem-solving skills and broadened my knowledge of artificial intelligence in games.

Roxana Ramazanova. Mtrc number: 72750731

For me, the hardest part of this chess project was that I am not good at playing chess and didn’t know the special rules of the game. 
Writing something big in Python was also new for me, as I have only worked on large projects in Java before. Additionally, using a Python game library was a new experience, which made the project even more challenging.
I worked on several parts of the chess engine. 
I implemented the moves for each piece, including their valid moves, and the logic for undoing moves. 
I also worked on the functions for generating all possible moves, checking for pins and checks, and the initiation of figures on the chessboard. 
However, I did not write the parts for en passant, pawn promotion, or castling.

Nijat Azizli. Mtrc number: 70825239

In this chess project, I worked on most of the frontend, like designing the board and writing the main() function, and also started the backend by creating the 2D array for the chessboard. 
The hardest part for me was that I have more experience in backend, so working on the frontend was new and challenging. 
I had to learn how to balance both parts to make everything work well.
Another big challenge was working as a team while being at least 30 kilometers apart. 
It was harder to communicate and coordinate our tasks remotely. 
Even with these challenges, I gained useful experience in frontend coding and teamwork.
