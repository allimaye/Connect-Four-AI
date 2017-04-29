from board import Board
from copy import deepcopy
from random import randint
import sys

class Connect4(object):

    def __init__(self, start_board, search_depth=5):
        # create a Board from a start board (2d array)
        self.root = Board(None, start_board)
        self.search_depth = search_depth
        self.root.maximizer = True

    def minimax(self):

        # edge case 1: CPU/maximizer/player 2 can win in 1 turn. Use a copy of the root board for this so it doesn't
        # interfere with alpha-beta pruning
        copy = deepcopy(self.root)
        copy.generate_child_boards()
        for board in copy.child_boards:
            if(board == None):
                continue
            if(board.p2_streaks[2] > 0):
                # (response board, if p2 has won)
                return (board.board, True, board.winning_streak)

        # edge case 2: Player 1 /human/mimimizer can win in 1 turn
        copy = deepcopy(self.root)
        copy.maximizer = False
        copy.generate_child_boards()
        for index, board in enumerate(copy.child_boards):
            if (board == None):
                continue
            if (board.p1_streaks[2] > 0):
                copy2 = deepcopy(self.root)
                copy2.generate_next_child(index)
                return (copy2.child_boards[0].board, False, None)


        # run minimax on the root board
        self.root.minimax(0, self.search_depth)

        # after minimax has finished running, the child boards will have a minimax value.
        # Since we know that root is always maximizer, pick the maximum minimax value
        max_val = -1 * sys.maxint
        correct_board_index = None
        for index, board in enumerate(self.root.child_boards):
            if (board == None):
                continue
            if (board.minimax_val > max_val):
                max_val = board.minimax_val
                correct_board_index = index

        # if there are no strategically sound boards available, then pick a random board.
        if(correct_board_index == None):
            correct_board_index = randint(0, len(self.root.child_boards) - 1)

        response_board = self.root.child_boards[correct_board_index].board
        return (response_board, False, None)

    def check_for_p1_win(self):
        # self.root.evaluate_board()
        if (self.root.p1_streaks[2] > 0):
            return (True, self.root.winning_streak)
        else:
            return (False, None)







