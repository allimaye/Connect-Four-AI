import re
from board import Board
from random import randint
from connect4 import Connect4
import time


def main():

    board = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0, 0, 0],
             [2, 0, 0, 1, 1, 1, 0]]

    streaks = find2_streaks234(board, 1)

    test_board = Board(None, board)
    test_board.maximizer = True
    print "Original board:"
    test_board.to_string()
    con4 = Connect4(board, 5)
    resp_board = con4.minimax()






    print "DONE"


def find_streaks234(board, player):

    # define 8 directions by how rows and column increment and decrement
    # format: [row, col]
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1], # N, E, S, W
            [-1, 1], [1, 1], [1, -1], [-1, -1]] # NE, SE, SW, NW

    streaks234 = [0,0,0]
    p = player

    for streak_length in xrange(2, 5):

        visited = []
        for row in board:
            new_row = []
            for col in row:
                new_row.append(False)
            visited.append(new_row)

        # traverse straight in all 8 directions from each point and
        # find any streaks that the point is a part of
        for row in xrange(0, 6):
            for col in xrange(0, 7):
                for dir in dirs:
                    is_streak = True
                    # dist_out starts at 0 so that board[row][col] == p is ensured
                    for dist_out in xrange(0, streak_length):
                        shift_row = row + dist_out*dir[0]
                        shift_col = col + dist_out*dir[1]
                        if not(shift_row in xrange(0, 6)) or \
                                not(shift_col in xrange(0, 7)) or \
                                visited[shift_row][shift_col] or \
                                board[shift_row][shift_col] != p:
                            is_streak = False
                            break

                    if is_streak:
                        streaks234[streak_length - 2] += 1

                visited[row][col] = True

    return streaks234

def find2_streaks234(board, player):

    # define 4 directions to search for N-streaks. Since we iterate by row and then by column,
    # other directions (N, NW, W, NE) don't need to be searched because we have already looked at those
    # elements in previous iterations.

    # format: [row_change, col_change]
    dirs = [[0, 1], [1, 0], [1, 1], [1, -1], ] # E, S, SE, SW

    streaks234 = [0,0,0]
    p = player
    streak4_coords = []

    for streak_length in xrange(2, 5):

        # traverse straight in all 4 directions from each point and
        # find any streaks that the current element is a part of
        for row in xrange(0, 6):
            for col in xrange(0, 7):
                for dir in dirs:
                    is_streak = True
                    # dist_out starts at 0 so that board[row][col] == p is ensured
                    for dist_out in xrange(0, streak_length):
                        shift_row = row + dist_out*dir[0]
                        shift_col = col + dist_out*dir[1]
                        if not(shift_row in xrange(0, 6)) or \
                                not(shift_col in xrange(0, 7)) or \
                                board[shift_row][shift_col] != p:
                            is_streak = False
                            break

                    if is_streak:
                        streaks234[streak_length - 2] += 1
                        # if this a winning streak, then record it
                        if(streak_length == 4):
                            for dist_out in xrange(0, 4):
                                shift_row = row + dist_out * dir[0]
                                shift_col = col + dist_out * dir[1]
                                streak4_coords.append([shift_row, shift_col])

    return streaks234








if __name__ == "__main__":
    main()