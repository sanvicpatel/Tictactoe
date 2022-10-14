"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0

    #counts number of X's and O's on board
    for row in board:
        for column in row:
            if column == "X":
                num_x += 1
            elif column == "O":
                num_o += 1

    if num_x > num_o:
        return O
    return X


    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    #creates a set that will contain tuples (i, j), representing positions where board is EMPTY
    set_of_moves = set()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                set_of_moves.add((row, column))

    return set_of_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #raises exception if the position at (i, j) already has an X or O
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("This action has already been taken")

    new_board = deepcopy(board)

    #returns a new board with an X or O (depending on whose turn) placed at the given position
    new_board[action[0]][action[1]] = player(new_board)
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #Checks for three X's or O's in a row
    for row in board:
        if row[0] == X and row[1] == X and row[2] == X:
            return X
        elif row[0] == O and row[1] == O and row[2] == O:
            return O

    #Checks for three X's or O's in a column
    for column in range(3):
        if board[0][column] == X and board[1][column] == X and board[2][column] == X:
            return X
        elif board[0][column] == O and board[1][column]== O and board[2][column] == O:
            return O

    #Checks for three X's or O's in a diagonal going from left to right
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O

    #Checks for three X's or O's in a diagonal going from right to left
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][2]== O and board[1][1] == O and board[2][0] == O:
        return O

    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    #If no winner, checks for an empty spot on the board. If there is one, returns false.
    for row in board:
        for column in row:
            if column == EMPTY:
                return False

    return True




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    #if it is X's turn, calls Min_Value on every possible action and records the best action
    #that yields the highest score
    if player(board) == X:
        score = -math.inf
        for action in actions(board):
            #passes score in Min_Value every time for alpha-beta pruning
            new_score = Min_Value(result(board, action), score)
            if new_score >= score:
                score = new_score
                best_action = action

    # if it is O's turn, calls Max_Value on every possible action and records the best action
    # that yields the lowest score
    else:
        score = math.inf
        for action in actions(board):
            #passes score in Max_Value every time for alpha-beta pruning
            new_score = Max_Value(result(board, action), score)
            if new_score <= score:
                score = new_score
                best_action = action

    return best_action


def Max_Value(board, score):
    """ Returns highest possible utility given a state and current value of score"""
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, Min_Value(result(board, action), score))
        #if v is higher than current value of score, returns v without checking other actions because
        #it is clear that Min_Value will not return a higher value than v at this point
        if v > score:
            return v
    return v

def Min_Value(board, score):
    """Returns lowest possible utility given a state and current value of score"""
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, Max_Value(result(board, action), score))
        #if v is lower than current value of score, returns v without checking other actions because
        #it is clear that Max_Value will not return a lower value than v at this point
        if v < score:
            return v
    return v