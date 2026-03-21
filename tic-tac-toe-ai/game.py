# Tic-Tac-Toe game logic: board state, move validation, win detection


class Board:
    # Represents a 3x3 Tic-Tac-Toe board

    def __init__(self):
        # Board is a flat list of 9 cells: None = empty, 'X' = human, 'O' = AI
        self.cells = [None] * 9
        self.current_player = 'X'  # X always goes first

    def get_available_moves(self):
        # Return indices of empty cells
        return [i for i, cell in enumerate(self.cells) if cell is None]

    def make_move(self, position):
        # Place current player's mark at position (0-8), return True if valid
        if position < 0 or position > 8:
            return False
        if self.cells[position] is not None:
            return False

        self.cells[position] = self.current_player
        # Switch turns
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def undo_move(self, position):
        # Undo a move (used by Minimax to explore states)
        self.cells[position] = None
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        # Return 'X', 'O', or None
        # All possible winning lines: rows, columns, diagonals
        win_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6],              # diagonals
        ]

        for line in win_lines:
            a, b, c = line
            if (self.cells[a] is not None
                    and self.cells[a] == self.cells[b]
                    and self.cells[b] == self.cells[c]):
                return self.cells[a]

        return None

    def is_full(self):
        # Check if the board has no empty cells
        return all(cell is not None for cell in self.cells)

    def is_terminal(self):
        # Check if the game is over (win or draw)
        return self.check_winner() is not None or self.is_full()

    def display(self):
        # Print the board to the terminal
        symbols = [cell if cell else str(i) for i, cell in enumerate(self.cells)]
        print()
        for row in range(3):
            start = row * 3
            print(f" {symbols[start]} | {symbols[start+1]} | {symbols[start+2]} ")
            if row < 2:
                print("-----------")
        print()