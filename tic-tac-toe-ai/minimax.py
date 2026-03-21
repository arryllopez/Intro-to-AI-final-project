# Minimax with Alpha-Beta Pruning — from-scratch AI for Tic-Tac-Toe

# Stats tracker to measure algorithm performance
stats = {
    'nodes_explored': 0,
    'pruned': 0,
    'max_depth': 0,
}


def reset_stats():
    # Reset performance counters
    stats['nodes_explored'] = 0
    stats['pruned'] = 0
    stats['max_depth'] = 0


def evaluate(board):
    # Score board from AI's perspective: +10 AI wins, -10 human wins, 0 otherwise
    winner = board.check_winner()
    if winner == 'O':
        return 10
    elif winner == 'X':
        return -10
    else:
        return 0


def minimax(board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf'), use_pruning=True):
    # Recursive minimax search with optional alpha-beta pruning
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
    # Find best move for AI by running minimax on all available moves
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