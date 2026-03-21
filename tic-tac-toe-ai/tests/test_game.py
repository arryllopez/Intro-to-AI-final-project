import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game import Board
from minimax import find_best_move, evaluate


# --- Board Tests ---

def test_empty_board():
    board = Board()
    assert board.get_available_moves() == list(range(9))
    assert board.check_winner() is None
    assert not board.is_full()
    print("PASS: empty board initialized correctly")


def test_make_move_switches_player():
    board = Board()
    assert board.current_player == 'X'
    board.make_move(0)
    assert board.current_player == 'O'
    board.make_move(1)
    assert board.current_player == 'X'
    print("PASS: make_move switches player correctly")


def test_invalid_move():
    board = Board()
    board.make_move(4)
    assert board.make_move(4) == False  # occupied cell
    assert board.make_move(-1) == False  # out of bounds
    assert board.make_move(9) == False   # out of bounds
    print("PASS: invalid moves rejected")


def test_undo_move():
    board = Board()
    board.make_move(0)
    board.undo_move(0)
    assert board.cells[0] is None
    assert board.current_player == 'X'
    print("PASS: undo_move restores state")


def test_win_detection():
    board = Board()
    # X wins top row: X at 0,1,2
    board.cells = ['X', 'X', 'X', 'O', 'O', None, None, None, None]
    assert board.check_winner() == 'X'

    # O wins diagonal
    board.cells = ['O', None, None, None, 'O', None, None, None, 'O']
    assert board.check_winner() == 'O'

    # No winner yet
    board.cells = ['X', 'O', 'X', None, None, None, None, None, None]
    assert board.check_winner() is None
    print("PASS: win detection works for rows, diagonals, and incomplete boards")


def test_draw():
    board = Board()
    board.cells = ['X', 'O', 'X',
                   'X', 'O', 'O',
                   'O', 'X', 'X']
    assert board.check_winner() is None
    assert board.is_full()
    assert board.is_terminal()
    print("PASS: draw detected correctly")


# --- Minimax Tests ---

def test_ai_blocks_win():
    # Human (X) is about to win on top row, AI (O) must block
    board = Board()
    board.cells = ['X', 'X', None,
                   'O', None, None,
                   None, None, None]
    board.current_player = 'O'
    move, stats = find_best_move(board)
    assert move == 2, f"AI should block at 2, got {move}"
    print(f"PASS: AI blocks human win (explored {stats['nodes_explored']} nodes)")


def test_ai_takes_win():
    # AI (O) has middle column (1,4), should complete it at 7
    board = Board()
    board.cells = ['X', 'O', None,
                   'X', 'O', None,
                   None, None, 'X']
    board.current_player = 'O'
    move, stats = find_best_move(board)
    assert move == 7, f"AI should win at 7, got {move}"
    print(f"PASS: AI takes winning move (explored {stats['nodes_explored']} nodes)")


def test_ai_never_loses():
    # Play a full game where AI goes second — it should never lose
    board = Board()
    for first_move in range(9):
        board.__init__()
        board.make_move(first_move)  # Human plays X

        while not board.is_terminal():
            move, _ = find_best_move(board)
            board.make_move(move)  # AI plays O

            if board.is_terminal():
                break

            # Human plays a random available move (worst case: first available)
            available = board.get_available_moves()
            if available:
                board.make_move(available[0])

        winner = board.check_winner()
        assert winner != 'X', f"AI lost when human opened at {first_move}"
    print("PASS: AI never loses across all 9 opening moves")


def test_pruning_reduces_nodes():
    board = Board()
    _, stats_pruned = find_best_move(board, use_pruning=True)
    _, stats_no_prune = find_best_move(board, use_pruning=False)
    assert stats_pruned['nodes_explored'] < stats_no_prune['nodes_explored']
    print(f"PASS: pruning explored {stats_pruned['nodes_explored']} vs {stats_no_prune['nodes_explored']} without")


# --- Run all tests ---

if __name__ == '__main__':
    test_empty_board()
    test_make_move_switches_player()
    test_invalid_move()
    test_undo_move()
    test_win_detection()
    test_draw()
    test_ai_blocks_win()
    test_ai_takes_win()
    test_ai_never_loses()
    test_pruning_reduces_nodes()
    print("\nAll tests passed!")
