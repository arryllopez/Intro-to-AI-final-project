# Tic-Tac-Toe with Minimax AI

A Tic-Tac-Toe game built to demonstrate adversarial search. The AI opponent uses the Minimax algorithm with Alpha-Beta pruning to play optimally. It cannot be beaten. Available in two versions: a terminal interface and a graphical UI.

## Setup and Run

**1. Clone the repository**

    git clone https://github.com/your-repo/Intro-to-AI-final-project.git
    cd Intro-to-AI-final-project/tic-tac-toe-ai

**2. Create a virtual environment**

    py -m venv env

**3. Activate the virtual environment**

On Windows:

    env\Scripts\activate

On Mac/Linux:

    source env/bin/activate

**4. Run the game**

Graphical interface (recommended):

    py ui.py

Terminal interface:

    py main.py

---

## How to Play
- You are X, the AI is O
- X always goes first
- In the terminal version, enter a number from 0 to 8 to place your mark
- In the graphical version, click any empty cell to place your mark

## Project Structure

| File | Description |
|------|-------------|
| ui.py | Graphical interface built with Tkinter |
| main.py | Terminal game loop. Handles player input and coordinates the board and AI |
| game.py | Board class. Manages game state, move validation, and win detection |
| minimax.py | AI logic. Implements Minimax with optional Alpha-Beta pruning |
| benchmark.py | Compares AI performance with and without Alpha-Beta pruning on the opening move |

## AI Details

At the start of each turn the AI simulates every possible game state from the current position all the way to the end of the game. It picks the move that guarantees the best outcome assuming the human also plays perfectly. If the human makes a mistake at any point, the AI spots the fastest path to a win and takes it.

The AI evaluates every possible game state before making a move using the following scoring:

- AI wins (O): +10
- Human wins (X): -10
- Draw: 0

A depth penalty is applied so the AI prefers to win in as few moves as possible and delays a loss as long as possible. Alpha-Beta pruning is enabled by default and cuts branches where the outcome cannot improve on an already known result.

After each AI move in the terminal version, the following stats are printed:
- Nodes explored
- Branches pruned
- Maximum search depth reached

---

## Options

Alpha-Beta pruning can be toggled off for comparison purposes. In main.py, change the find_best_move call:

    move, ai_stats = find_best_move(board, use_pruning=False)

This will produce identical moves but explore significantly more nodes, useful for seeing the performance difference pruning makes.

---

## Outcome

The AI plays perfectly in all cases. Against optimal human play the game always ends in a draw. Against any suboptimal play the AI wins. It is not possible for the human to win.