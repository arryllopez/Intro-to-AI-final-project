# Tic-Tac-Toe: Human vs AI (Terminal Version)

from game import Board
from minimax import find_best_move


def play():
    board = Board()

    print("=== Tic-Tac-Toe: Human (X) vs AI (O) ===")
    print("Enter a number 0-8 to place your mark:")
    print()
    print(" 0 | 1 | 2 ")
    print("-----------")
    print(" 3 | 4 | 5 ")
    print("-----------")
    print(" 6 | 7 | 8 ")
    print()

    while not board.is_terminal():
        board.display()

        if board.current_player == 'X':
            # Human's turn
            while True:
                try:
                    move = int(input("Your move (0-8): "))
                    if board.make_move(move):
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, EOFError):
                    print("Enter a number 0-8.")
        else:
            # AI's turn
            print("AI is thinking...")
            move, ai_stats = find_best_move(board, use_pruning=True)
            board.make_move(move)
            print(f"AI plays position {move}")
            print(f"  [Nodes explored: {ai_stats['nodes_explored']}, "
                  f"Pruned: {ai_stats['pruned']}, "
                  f"Max depth: {ai_stats['max_depth']}]")

    # Game over
    board.display()
    winner = board.check_winner()
    if winner == 'X':
        print("You win! (Shouldn't be possible against perfect play...)")
    elif winner == 'O':
        print("AI wins!")
    else:
        print("It's a draw!")


if __name__ == '__main__':
    play()