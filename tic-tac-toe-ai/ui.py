# Tic-Tac-Toe AI — Tkinter GUI

import tkinter as tk
from game import Board
from minimax import find_best_move


class TicTacToeGUI:
    def __init__(self):
        self.board = Board()

        # Window setup
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe AI")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Title
        self.title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe AI",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4",
        )
        self.title_label.pack(pady=(15, 5))

        # Status label (whose turn / winner)
        self.status_label = tk.Label(
            self.root,
            text="Your turn (X)",
            font=("Helvetica", 14),
            bg="#1e1e2e",
            fg="#a6e3a1",
        )
        self.status_label.pack(pady=(0, 10))

        # Board frame
        self.board_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.board_frame.pack(padx=20)

        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Helvetica", 32, "bold"),
                width=3,
                height=1,
                bg="#313244",
                fg="#cdd6f4",
                activebackground="#45475a",
                relief="flat",
                borderwidth=2,
                command=lambda pos=i: self.human_move(pos),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)

        # Stats frame
        self.stats_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.stats_frame.pack(pady=(10, 5))

        self.stats_label = tk.Label(
            self.stats_frame,
            text="Nodes: —  |  Pruned: —  |  Depth: —",
            font=("Helvetica", 10),
            bg="#1e1e2e",
            fg="#6c7086",
        )
        self.stats_label.pack()

        # Reset button
        self.reset_btn = tk.Button(
            self.root,
            text="New Game",
            font=("Helvetica", 12),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            relief="flat",
            padx=20,
            pady=5,
            command=self.reset,
        )
        self.reset_btn.pack(pady=(5, 15))

        self.game_over = False

    def human_move(self, position):
        # Handle a human click on a cell
        if self.game_over:
            return
        if self.board.current_player != 'X':
            return
        if not self.board.make_move(position):
            return

        self.update_button(position, 'X')

        if self.check_game_over():
            return

        # AI responds after a short delay so the UI feels natural
        self.status_label.config(text="AI thinking...", fg="#f9e2af")
        self.root.after(100, self.ai_move)

    def ai_move(self):
        # AI picks and plays its move
        move, ai_stats = find_best_move(self.board, use_pruning=True)
        self.board.make_move(move)
        self.update_button(move, 'O')

        # Update stats display
        self.stats_label.config(
            text=f"Nodes: {ai_stats['nodes_explored']}  |  "
                 f"Pruned: {ai_stats['pruned']}  |  "
                 f"Depth: {ai_stats['max_depth']}"
        )

        if self.check_game_over():
            return

        self.status_label.config(text="Your turn (X)", fg="#a6e3a1")

    def update_button(self, position, player):
        # Update button text and color after a move
        color = "#89b4fa" if player == 'X' else "#f38ba8"
        self.buttons[position].config(text=player, fg=color, state="disabled")

    def check_game_over(self):
        # Check for win/draw and update status label
        winner = self.board.check_winner()
        if winner:
            self.game_over = True
            if winner == 'X':
                self.status_label.config(text="You win!", fg="#a6e3a1")
            else:
                self.status_label.config(text="AI wins!", fg="#f38ba8")
            self.highlight_winner()
            return True
        if self.board.is_full():
            self.game_over = True
            self.status_label.config(text="Draw!", fg="#f9e2af")
            return True
        return False

    def highlight_winner(self):
        # Highlight the winning line
        win_lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        for line in win_lines:
            a, b, c = line
            if (self.board.cells[a] is not None
                    and self.board.cells[a] == self.board.cells[b]
                    and self.board.cells[b] == self.board.cells[c]):
                for idx in line:
                    self.buttons[idx].config(bg="#585b70")
                return

    def reset(self):
        # Reset board for a new game
        self.board = Board()
        self.game_over = False
        self.status_label.config(text="Your turn (X)", fg="#a6e3a1")
        self.stats_label.config(text="Nodes: —  |  Pruned: —  |  Depth: —")
        for btn in self.buttons:
            btn.config(text="", fg="#cdd6f4", bg="#313244", state="normal")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TicTacToeGUI()
    app.run()