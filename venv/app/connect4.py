from board import Board
from copy import deepcopy
import sys

class Connect4(object):

    def __init__(self, start_board, search_depth=5):
        # create a Board from a start board (2d array)
        self.root = Board(None, start_board)
        self.search_depth = search_depth
        self.root.maximizer = True

    def minimax(self):

        # edge case: can win in 1 turn. Use a copy of the root board for this so it doesn't
        # interfere with alpha-beta pruning
        copy = deepcopy(self.root)
        copy.generate_child_boards()
        for board in copy.child_boards:
            if(board == None):
                continue
            board.evaluate_board()
            if(board.p2_streaks[2] > 0):
                # (response board, if p2 has won)
                return (board.board, True)

        # run minimax on the root board
        self.root.minimax(0, self.search_depth)

        # after minimax has finished running, the child boards will have a minimax value.
        # Since we know that root is always maximizer, pick the max one
        max_val = -1 * sys.maxint
        correct_board_index = None
        for index, board in enumerate(self.root.child_boards):
            if (board == None):
                continue
            if (board.minimax_val > max_val):
                max_val = board.minimax_val
                correct_board_index = index

        response_board = self.root.child_boards[correct_board_index].board
        return (response_board, False)

    def check_for_p1_win(self):
        self.root.evaluate_board()
        if (self.root.p1_streaks[2] > 0):
            return True







