import re
from board import Board
from random import randint
from connect4 import Connect4


def main():
    # x = "2202202202"
    # y = re.findall(r'(?=(2202))', x)
    #
    # z = "220022021310130"
    #
    # zero_pos = []
    # for index, char in enumerate(z):
    #     if char == "0":
    #         zero_pos.append(index)

    # board = []
    # for row in xrange(0, 6):
    #     if(row < 4):
    #         board.append([0]*7)
    #         continue
    #
    #     board_row = []
    #     for col in xrange(0, 7):
    #         board_row.append(randint(0,2))
    #     board.append(board_row)

    board = [[2, 2, 2, 1, 1, 0, 0],
             [2, 1, 2, 1, 1, 0, 0],
             [2, 1, 2, 1, 1, 1, 0],
             [1, 2, 1, 2, 2, 2, 0],
             [1, 2, 2, 2, 1, 2, 0],
             [1, 1, 2, 1, 2, 1, 1]]

    test_board = Board(None, board)
    test_board.maximizer = True
    print "Original board:"
    test_board.to_string()

    # test_board.evaluate_board()

    # test_board.generate_child_boards()
    # for index, board in enumerate(test_board.child_boards):
    #     print "\nChild board %s:\n" % index
    #     board.to_string()

    con4 = Connect4(board, 5)
    resp_board = con4.minimax()
    # while True:
    #     test_board.generate_next_child()


    print "DONE"



    pass

if __name__ == "__main__":
    main()