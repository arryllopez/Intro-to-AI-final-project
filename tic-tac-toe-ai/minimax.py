"""
Minimax Algorithm with Alpha-Beta Pruning
Implements the core AI decision-making for Tic-Tac-Toe.

No external AI/ML libraries used — this is a from-scratch implementation
of the Minimax search algorithm with optional Alpha-Beta pruning.
"""

# Stats tracker to measure algorithm performance
stats = {
    'nodes_explored': 0,
    'pruned': 0,
    'max_depth': 0,
}


def reset_stats():
    """Reset the performance counters."""
    stats['nodes_explored'] = 0
    stats['pruned'] = 0
    stats['max_depth'] = 0


def evaluate(board):
    """
    Evaluate the board from the AI's perspective (AI = 'O').
    Returns:
        +10 if AI wins
        -10 if Human wins
          0 if draw or game not over
    """
    winner = board.check_winner()
    if winner == 'O':
        return 10
    elif winner == 'X':
        return -10
    else:
        return 0


def minimax(board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf'), use_pruning=True):
    """
    Minimax with optional Alpha-Beta pruning.

    Parameters:
        board:          the current Board object
        depth:          current depth in the game tree
        is_maximizing:  True if it's the AI's turn (maximizer), False for human (minimizer)
        alpha:          best score the maximizer can guarantee (for pruning)
        beta:           best score the minimizer can guarantee (for pruning)
        use_pruning:    set False to run pure Minimax without pruning (for comparison)

    Returns:
        The evaluated score of the board state.
    """
    stats['nodes_explored'] += 1
    stats['max_depth'] = max(stats['max_depth'], depth)

    # Base case: terminal state reached
    score = evaluate(board)
    if score != 0:
        # Prefer faster wins / slower losses by adjusting with depth
        return score - depth if score > 0 else score + depth
    if board.is_full():
        return 0

    available = board.get_available_moves()

    if is_maximizing:
        # AI's turn — maximize score
        best_score = float('-inf')
        for move in available:
            board.make_move(move)
            move_score = minimax(board, depth + 1, False, alpha, beta, use_pruning)
            board.undo_move(move)

            best_score = max(best_score, move_score)

            if use_pruning:
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    stats['pruned'] += 1
                    break  # Beta cutoff — minimizer won't allow this path

        return best_score

    else:
        # Human's turn — minimize score
        best_score = float('inf')
        for move in available:
            board.make_move(move)
            move_score = minimax(board, depth + 1, True, alpha, beta, use_pruning)
            board.undo_move(move)

            best_score = min(best_score, move_score)

            if use_pruning:
                beta = min(beta, best_score)
                if beta <= alpha:
                    stats['pruned'] += 1
                    break  # Alpha cutoff — maximizer won't allow this path

        return best_score


def find_best_move(board, use_pruning=True):
    """
    Determine the best move for the AI ('O') by running Minimax on all available moves.

    Returns:
        (best_position, stats_dict) — the optimal move index and performance stats.
    """
    reset_stats()

    best_score = float('-inf')
    best_move = None

    for move in board.get_available_moves():
        board.make_move(move)
        score = minimax(board, 0, False, use_pruning=use_pruning)
        board.undo_move(move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, dict(stats)