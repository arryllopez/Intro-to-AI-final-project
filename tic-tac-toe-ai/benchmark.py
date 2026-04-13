from game import Board
from minimax import find_best_move

board = Board()

_, stats_pruned = find_best_move(board, use_pruning=True)
_, stats_no_prune = find_best_move(board, use_pruning=False)

print(f"With pruning:    {stats_pruned}")
print(f"Without pruning: {stats_no_prune}")