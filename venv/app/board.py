import re
import sys
from copy import deepcopy

class Board(object):

    def __init__(self, parent_board, board, alpha=float("-inf"), beta=float("inf")):
        self.parent_board = parent_board
        self.board = board
        self.child_boards = []
        # [2-streaks, 3-streaks, 4-streaks, nullifiers]
        self.p1_streaks = [0, 0, 0]
        self.p1_threats = 0
        self.p1_nullifiers = 0
        self.p2_streaks = [0, 0, 0]
        self.p2_threats = 0
        self.p2_nullifiers = 0
        self.winning_streak = []
        self.minimax_val = 0
        self.maximizer = None
        self.alpha = alpha
        self.beta = beta


    def minimax(self, depth, search_depth):

        # ------ base case: leaf node -----------
        if(depth == search_depth):
            self.evaluate_board()
            return

        # -------- non leaf node -----------

        # assign a min value to the maximizer and a max value to the minimizer
        if(self.maximizer):
            self.minimax_val = 0
        else:
            self.minimax_val = sys.maxint * 10

        for col in xrange(0, 7):
            # generate the next child and pass on alpa and beta values.
            # If a child cannot be created (since the corresponding column is full), move on to next child.
            board_created = self.generate_next_child(col)
            if(not board_created):
                continue

            curr_child = self.child_boards[col]
            curr_child.minimax(depth + 1, search_depth)

            # update alpha/beta and minimax values based on child
            if(self.maximizer):
                if(curr_child.minimax_val > self.alpha):
                    self.alpha = curr_child.minimax_val
                if(curr_child.minimax_val >= self.minimax_val):
                    self.minimax_val = curr_child.minimax_val
            else:
                if(curr_child.minimax_val < self.beta):
                    self.beta = curr_child.minimax_val
                if (curr_child.minimax_val < self.minimax_val):
                    self.minimax_val = curr_child.minimax_val

            # prune any nodes that don't need to be searched
            if(self.alpha >= self.beta):
                break

        # If at this point all child boards are null boards, then we have reached a leaf node that is not
        # at the search depth. This would correspond to the last possible move. Since my search depth will never
        # be high enough to reach this point, exclude the code to improve performance.

    # generate the opposing player's responses to this board
    def generate_child_boards(self):
        if(len(self.child_boards) == 7):
            return

        for col in xrange(0, 7):
            for row in xrange(5, -1, -1):
                if(self.board[row][col] == 0):
                    child_board = deepcopy(self.board)
                    new_board = None
                    # the current board belongs to player 1, so player 2 (CPU) will make the next move
                    if(self.maximizer):
                        child_board[row][col] = 2
                        new_board = Board(self, child_board)
                        new_board.maximizer = False
                    else:
                        child_board[row][col] = 1
                        new_board = Board(self, child_board)
                        new_board.maximizer = True

                    self.child_boards.append(new_board)
                    break

    def generate_next_child(self, colNum):
        # all childs have been generated (cannot generate another child)
        if (len(self.child_boards) == 7):
            return False

        for row in xrange(5, -1, -1):
            if (self.board[row][colNum] == 0):
                child_board = deepcopy(self.board)
                new_board = Board(self, child_board, self.alpha, self.beta)
                # the current board belongs to player 1, so player 2 (CPU) will make the next move
                if (self.maximizer):
                    child_board[row][colNum] = 2
                    new_board.maximizer = False
                else:
                    child_board[row][colNum] = 1
                    new_board.maximizer = True

                self.child_boards.append(new_board)
                return True

        # this means that a child board could not be generated for this column because the column was full.
        # Move on to the next column during next call. Append a null board for this case.
        self.child_boards.append(None)
        return False


    def evaluate_board(self):

        # find all 2-,3-, and 4-streaks for both players
        self.find_streaks234(1)
        self.find_streaks234(2)

        # Take weighted average using each of the heuristics.
        # Priority from highest to lowest:
        # 1. Prevent a losing board. If any board has a 4-streak for p1, then it gets -inf value
        # 2. Get as many 234 streaks as possible. The value of 2-streaks < 3-streaks << 4-streaks

        self.minimax_val = 2*self.p2_streaks[0] + 4*self.p2_streaks[1] + 100*self.p2_streaks[2]
        if(self.p1_streaks[2] > 0):
            self.minimax_val = -1 * sys.maxint


    def find_streaks234(self, player):

        # define 4 directions to search for N-streaks. Since we iterate by row and then by column,
        # other directions (N, NW, W, NE) don't need to be searched because we have already looked at those
        # elements in previous iterations.

        # format: [row, col]
        dirs = [[0, 1], [1, 0], [1, 1], [1, -1], ]  # E, S, SE, SW

        for streak_length in xrange(2, 5):
            # traverse straight in all 4 directions from each point and
            # find any streaks that the current element is a part of
            for row in xrange(0, 6):
                for col in xrange(0, 7):
                    for dir in dirs:
                        is_streak = True
                        # dist_out starts at 0 so that board[row][col] == p is ensured
                        for dist_out in xrange(0, streak_length):
                            shift_row = row + dist_out * dir[0]
                            shift_col = col + dist_out * dir[1]
                            if not (shift_row in xrange(0, 6)) or \
                                    not (shift_col in xrange(0, 7)) or \
                                    self.board[shift_row][shift_col] != player:
                                is_streak = False
                                break

                        if is_streak:
                            if(player == 1):
                                self.p1_streaks[streak_length - 2] += 1
                            else:
                                self.p2_streaks[streak_length - 2] += 1

                            # if this a winning streak, then record it
                            if (streak_length == 4):
                                for dist_out in xrange(0, 4):
                                    shift_row = row + dist_out * dir[0]
                                    shift_col = col + dist_out * dir[1]
                                    self.winning_streak.append([shift_row, shift_col])


    def to_string(self):
        for row in self.board:
            for val in row:
                print '{:4}'.format(val),
            print





    #
    #
    #
    # # define a winning row as any set of 4 adjacent squares where p2 has one piece and p1 has no pieces
    # # find the number of winning rows for player 2 originating from a specific square
    # def winning_rows(self, x, y):
    #     # a winning row can only form if this square is claimed by p2 (to avoid double counting)
    #     if self.board[x][y] != 2:
    #         return 0
    #
    #     #check the number of winning rows originating from this piece. Check all directions (including diagonals)
    #     winning_rows = 0
    #     N_found = False
    #     NE_found = False
    #     E_found = False
    #     SE_found = False
    #     S_found = False
    #     SW_found = False
    #     W_found = False
    #     NW_found = False
    #
    #     for i in xrange(0, 3):
    #         try:
    #             # N
    #             if(self.board[x][y - i] == 1 and not N_found):
    #                 N_found = True
    #                 winning_rows += 1
    #             # NE
    #             if (self.board[x + i][y - i] == 1 and not NE_found):
    #                 NE_found = True
    #                 winning_rows += 1
    #             # E
    #             if (self.board[x + i][y] == 1 and not E_found):
    #                 E_found = True
    #                 winning_rows += 1
    #             # SE
    #             if (self.board[x + i][y + i] == 1 and not SE_found):
    #                 SE_found = True
    #                 winning_rows += 1
    #             # S
    #             if (self.board[x][y + i] == 1 and not S_found):
    #                 S_found = True
    #                 winning_rows += 1
    #             # SW
    #             if (self.board[x - i][y + i] == 1 and not SW_found):
    #                 SW_found = True
    #                 winning_rows += 1
    #             # W
    #             if (self.board[x - i][y] == 1 and not W_found):
    #                 W_found = True
    #                 winning_rows += 1
    #             # NW
    #             if (self.board[x - i][y - i] == 1 and not NW_found):
    #                 NW_found = True
    #                 winning_rows += 1
    #
    #         except IndexError:
    #             pass
    #
    #     return winning_rows
    #
    # def threats_and_streaks(self):
    #
    #     # find all the threats and streaks in diagonals (diagonals with less than 4 squares will be ignored)
    #
    #     # positive slope diagonals
    #     for x in xrange(3, 6):
    #         sequence, start_point = self.get_diagonal_sequence(x, 0, "+")
    #         self.threats_in_sequence(sequence)
    #         self.streaks_234(sequence, (start_point, "diagonal", "+"))
    #         self.nullifiers_in_sequence(sequence)
    #     for y in xrange(1, 4):
    #         sequence, start_point = self.get_diagonal_sequence(5, y, "+")
    #         self.threats_in_sequence(sequence)
    #         self.streaks_234(sequence, (start_point, "diagonal", "+"))
    #         self.nullifiers_in_sequence(sequence)
    #
    #     # negative slope diagonals
    #     for x in xrange(2, -1, -1):
    #         sequence, start_point = self.get_diagonal_sequence(x, 0, "-")
    #         self.threats_in_sequence(sequence)
    #         self.streaks_234(sequence, (start_point, "diagonal", "-"))
    #         self.nullifiers_in_sequence(sequence)
    #     for y in xrange(1, 4):
    #         sequence, start_point = self.get_diagonal_sequence(0, y, "-")
    #         self.threats_in_sequence(sequence)
    #         self.streaks_234(sequence, (start_point, "diagonal", "-"))
    #         self.nullifiers_in_sequence(sequence)
    #
    #     # rows
    #     for index, row in enumerate(self.board):
    #         self.threats_in_sequence(row)
    #         # self.streaks_234(row)
    #         self.streaks_234(row, ([index, 0], "row", None))
    #         self.nullifiers_in_sequence(row)
    #
    #     # columns
    #     for colNum in xrange(0, 7):
    #         col = []
    #         for row in self.board:
    #             col.append(row[colNum])
    #         self.threats_in_sequence(col)
    #         # self.streaks_234(col)
    #         self.streaks_234(col, ([0, colNum], "col", None))
    #         self.nullifiers_in_sequence(col)
    #
    # def streaks_234(self, sequence, streak_info):
    #     # join all ints from sequence array into a string
    #     joined = ""
    #     for piece in sequence:
    #         joined = joined + str(piece)
    #
    #     # --------------- Player 2's 234 streaks ----------------------------------------------
    #     # search for all possible streak patterns (2 pieces in a row, 3 pieces in a row,
    #     # and 4 pieces in a row)
    #     for i in xrange(2, 5):
    #         search_str = "2"*i
    #         # no overlaps allowed in pattern matching
    #         matches = re.findall(search_str, joined)
    #         self.p2_streaks[i-2] += len(matches)
    #         if(i == 4 and len(matches) > 0):
    #             streak_start = re.search(search_str, joined).start(0)
    #             self.record_streak(streak_start, streak_info)
    #
    #     # --------------- Player 1's 234 streaks ----------------------------------------------
    #
    #     for i in xrange(2, 5):
    #         search_str = "1" * i
    #         # no overlaps allowed in pattern matching
    #         matches = re.findall(search_str, joined)
    #         self.p1_streaks[i - 2] += len(matches)
    #         if (i == 4 and len(matches) > 0):
    #             streak_start = re.search(search_str, joined).start(0)
    #             self.record_streak(streak_start, streak_info)
    #
    # def record_streak(self, streak_start, streak_info):
    #     win_streak = []
    #     # streak_info = (bounds, direction, slope)
    #     start_row = streak_info[0][0]
    #     start_col = streak_info[0][1]
    #     if(streak_info[1] == "diagonal"):
    #         for shift in xrange(streak_start, streak_start + 4):
    #             if (streak_info[2] == "+"):
    #                 win_streak.append([start_row - shift, start_col + shift])
    #             elif(streak_info[2] == "-"):
    #                 win_streak.append([start_row + shift, start_col + shift])
    #     elif(streak_info[1] == "row"):
    #         for col in xrange(streak_start, streak_start + 4):
    #             win_streak.append([start_row, col])
    #     elif (streak_info[1] == "col"):
    #         for row in xrange(streak_start, streak_start + 4):
    #             win_streak.append([row, start_col])
    #
    #     self.winning_streak = win_streak
    #
    #
    # # positive-slope and negative-slope diagonals
    # def get_diagonal_sequence(self, start_x, start_y, slope):
    #     sequence = []
    #     counter = 0
    #     while(True):
    #         row = start_x - counter
    #         col = start_y + abs(counter)
    #         if not(row in range(0, 6)) or not(col in range(0, 7)):
    #             # return the starting and ending coordinates of this sequence
    #             return (sequence, [start_x, start_y])
    #
    #         sequence.append(self.board[row][col])
    #         if slope == "+":
    #             counter += 1
    #         else:
    #             counter -= 1
    #
    # def threats_in_sequence(self, sequence):
    #
    #     # join all ints from sequence array into a string
    #     joined = ""
    #     for piece in sequence:
    #         joined = joined + str(piece)
    #
    #     #--------------- Player 2's threats ----------------------------------------------
    #     # search for all possible threat patterns where exactly 3 of player 2's pieces
    #     # are there and none of p1ayer 1's
    #     matched = 0
    #     for i in xrange(0,4):
    #         pattern = list("2222")
    #         pattern[i] = "0"
    #         search_str = "".join(pattern)
    #         # allow overlap in pattern matching
    #         matches = re.findall(r'(?=(%s))' % (search_str), joined)
    #         matched += len(matches)
    #
    #     # search the number of zeros in the sequence. The number of threats should be
    #     # less than or equal to the number of zeros.
    #     zeros = len(re.findall("0", joined))
    #     if matched > zeros:
    #         self.p2_threats += zeros
    #     else:
    #         self.p2_threats += matched
    #
    #
    #     # --------------- Player 1's threats --------------------------------------------
    #     matched = 0
    #     for i in xrange(0, 4):
    #         pattern = list("1111")
    #         pattern[i] = "0"
    #         search_str = "".join(pattern)
    #         # allow overlap in pattern matching
    #         matches = re.findall(r'(?=(%s))' % (search_str), joined)
    #         matched += len(matches)
    #
    #     # search the number of zeros in the sequence. The number of threats should be
    #     # less than or equal to the number of zeros.
    #     zeros = len(re.findall("0", joined))
    #     if matched > zeros:
    #         self.p1_threats += zeros
    #     else:
    #         self.p1_threats += matched
    #
    # def nullifiers_in_sequence(self, sequence):
    #     # join all ints from sequence array into a string
    #     joined = ""
    #     for piece in sequence:
    #         joined = joined + str(piece)
    #
    #     # --------------- Player 2's nullifiers ----------------------------------------------
    #     # search for all possible patterns where exactly 1 of player 2's pieces
    #     # nullifies a threat from p1
    #     matched = 0
    #     for i in xrange(0, 4):
    #         pattern = list("1111")
    #         pattern[i] = "2"
    #         search_str = "".join(pattern)
    #         # allow overlap in pattern matching
    #         matches = re.findall(r'(?=(%s))' % (search_str), joined)
    #         matched += len(matches)
    #
    #     # search the number of p2's pieces in the sequence. The number of nullifies should be
    #     # less than or equal to the number of 2s.
    #     twos = len(re.findall("2", joined))
    #     if matched > twos:
    #         self.p2_nullifiers += twos
    #     else:
    #         self.p2_nullifiers += matched
    #
    #     # --------------- Player 1's nullifiers --------------------------------------------
    #     matched = 0
    #     for i in xrange(0, 4):
    #         pattern = list("2222")
    #         pattern[i] = "1"
    #         search_str = "".join(pattern)
    #         # allow overlap in pattern matching
    #         matches = re.findall(r'(?=(%s))' % (search_str), joined)
    #         matched += len(matches)
    #
    #     ones = len(re.findall("1", joined))
    #     if matched > ones:
    #         self.p1_nullifiers += ones
    #     else:
    #         self.p1_nullifiers += matched

