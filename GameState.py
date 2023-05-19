from typing import NamedTuple
from numpy import ndarray

class GameState(NamedTuple):
    """
    board_status: int[][]
        Absolute element  ==  4     :      Square taken by a player
        Element's sign    ==  +     :      Square taken by player 1
        Element's sign    ==  -     :      Square taken by player 2
        Access: board_status[y, x]

    row_status: int[][]
        Horizontal line mark status:
            1 : marked,
            0 : not.
        How to access: row_status[y, x]

    col_status: int[][]
        Vertical line mark status:
            1 : marked,
            0 : not.
        How to access: col_status[y, x]
        
    player1_turn: bool
        True    :    player 1 turn,
        False   :    player 2 turn.
    """

    board_status: ndarray
    row_status: ndarray
    col_status: ndarray
    player1_turn: bool
