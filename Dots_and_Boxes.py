from copy import deepcopy
from math import inf
from tkinter import Canvas
from tkinter.tix import Tk
from typing import Optional
from random import shuffle
import time

from GameState import GameState
import numpy as np
from GameAction import GameAction

loop = False
NUMBER_OF_DOTS = 8
CPU_DELAY_MS = 1

BOARD_SIZE = 600
SYMBOL_SIZE = (BOARD_SIZE / 3 - BOARD_SIZE / 8) / 2
SYMBOL_THICKNESS = 50
DOT_COLOR = '#7BC043'
P1_COLOR = '#0492CF'
P1_COLOR_LM = '#67B0CF'
P2_COLOR = '#EE4035'
P2_COLOR_LM = '#EE7E77'
COLOR_GREEN = '#7BC043'
DOT_WIDTH = 0.25 * BOARD_SIZE / NUMBER_OF_DOTS
EDGE_WIDTH = 0.1 * BOARD_SIZE / NUMBER_OF_DOTS
DOTS_DISTANCE = BOARD_SIZE / NUMBER_OF_DOTS

LEFT_CLICK = '<Button-1>'

start = time.time()


def get_valid_neighbors(cell, board, rows, cols):
    """
    It returns all valid cells around the passed one
    (a cell is considered valid only if it hasn't been completed and isn't
    separated by a line from the passed cell)

    :param cell: The cell of which find valid neighbors
    :param board: The game board
    :param rows: The game line rows
    :param cols: The game line cols
    :return: A list containing all valid neighbors cells
    """
    x, y = cell
    neighbors = []
    if abs(board[x][y]) == 4:
        return neighbors
    if y < len(board[0]) - 1 and abs(board[x][y + 1]) <= 3 and cols[x][y + 1] != 1:
        neighbors.append((x, y + 1))
    if y > 0 and abs(board[x][y - 1]) <= 3 and cols[x][y] != 1:
        neighbors.append((x, y - 1))
    if x < len(board) - 1 and abs(board[x + 1][y]) <= 3 and rows[x + 1][y] != 1:
        neighbors.append((x + 1, y))
    if x > 0 and abs(board[x][y]) <= 3 and rows[x][y] != 1:
        neighbors.append((x - 1, y))
    return neighbors


def dfs(cell, board, rows, cols, visited, chain):
    """
    It applies a depth first search from a desired cell to find all possible chains

    :param cell: The starting cell
    :param board: The game board
    :param rows: The game line rows
    :param cols: The game line cols
    :param visited: A list of all visited cells
    :param chain: A list which contains the founded chain
    """
    visited.add(cell)
    chain.append(cell)

    neighbors = get_valid_neighbors(cell, board, rows, cols)

    if len(neighbors) == 0 or set(neighbors) <= visited:
        return True

    for neighbor in neighbors:
        if neighbor not in visited:
            x, y = neighbor
            if abs(board[x][y]) == 4:
                return True
            elif abs(board[x][y]) <= 3:
                if dfs(neighbor, board, rows, cols, visited, chain):
                    return True


def find_chains(board, rows, cols):
    """
    It finds all possible chains on the board

    :param board: The game board
    :param rows: The game line rows
    :param cols: The game line cols
    :return: The list of all possible chains on the board
    """
    chains = []
    visited = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            cell = (row, col)
            if abs(board[row][col]) <= 3 and cell not in visited:
                chain = []
                if dfs(cell, board, rows, cols, visited, chain):
                    chains.append(chain)

    return chains


def find_long_chains(board, rows, cols):
    """
    It finds all possible long chains on the board
    (a long chain is a chain containing at least 3 cells)

    :param board: The game board
    :param rows: The game line rows
    :param cols: The game line cols
    :return: The list of all possible long chains on the board
    """
    return sorted([lst for lst in find_chains(board, rows, cols) if len(lst) > 3], key=len, reverse=True)


def check_single_4(board):
    """
    It checks if there is only one completed cell (obtained by a player)

    :param board: The game board
    :return: True: only one cell has been completed; False: otherwise
    """
    count = 0
    for row in board:
        for value in row:
            if abs(value) == 4:
                count += 1
    return count == 1


def check_no_4(board):
    """
    It checks if there aren't any completed cell (obtained by a player)

    :param board: The game board
    :return: True: only no cells has been completed; False: otherwise
    """
    count = 0
    for row in board:
        for value in row:
            if abs(value) == 4:
                count += 1
    return count == 0


class CPU:

    def get_action(self, game, is_player1, player_1_stars) -> GameAction:
        """
        It chooses a move from all available ones

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: The chosen move
        """
        raise NotImplementedError()


class AlphaBetaCPU(CPU):

    def __init__(self, max_depth=3):
        self.MAX_DEPTH = max_depth

    def get_valid_moves(self, game):
        """
        It finds all valid moves on the board
        :param game: The Dot and Boxes match instance
        :return: A list containing all the possible moves on the board
        """
        state = game.get_game_state()

        valid_rows_moves = []
        for i in range(0, len(state.row_status), 1):
            for j in range(0, len(state.row_status[i]), 1):
                if state.row_status[i][j] == 0.:
                    valid_rows_moves.append(GameAction("row", (j, i)))

        valid_cols_moves = []
        for i in range(0, len(state.col_status), 1):
            for j in range(0, len(state.col_status[i]), 1):
                if state.col_status[i][j] == 0.:
                    valid_cols_moves.append(GameAction("col", (j, i)))
        l = valid_rows_moves + valid_cols_moves
        shuffle(l)
        return l

    def get_action(self, game, is_player1, player_1_stars) -> GameAction:
        """
        It chooses a move from all available ones

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: The chosen move
        """
        game_copy = game
        move = self.alphabeta(game_copy, is_player1, player_1_stars)[0]
        return move

    def evaluate_goodness(self, game, is_player1, player_1_stars):
        """
        Evaluate how good is the board setting for a player

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: A score representing how good the board setting is for a player
        """
        raise NotImplementedError()

    def alphabeta(self, game, is_player1=False, player_1_stars=True, depth=None, alpha=-inf, beta=inf, is_max=True,
                  move=GameAction("row", (0, 0))):
        """
        It runs the alphabeta algorithm to find the best move possible
        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :param depth: Moves tree's current depth
        :param alpha: Alpha parameter
        :param beta: Beta parameter
        :param is_max: If the algorithm must be run in max mode or min one
        :return: The chosen move (best of worse)
        """
        children = self.get_valid_moves(game)

        if depth is None:
            depth = self.MAX_DEPTH

        if depth == 0 or len(children) == 0:
            return [move, self.evaluate_goodness(game, is_player1, player_1_stars)]

        if is_max:
            best_move = ()
            best_score = -inf
            for move in children:
                game_copy = game.get_copy()
                point_scored = game_copy.update_board(move.action_type, move.position, is_player1)
                temp = self.alphabeta(game_copy, is_player1, player_1_stars,
                                      depth - 1, alpha, beta,
                                      point_scored, move)
                if temp[1] > best_score:
                    best_move = move
                    best_score = temp[1]
                alpha = max(best_score, alpha)
                if beta <= alpha:
                    break
            return [best_move, best_score]
        else:
            worse_move = ()
            worse_score = inf
            for move in children:
                game_copy = game.get_copy()
                point_scored = game_copy.update_board(move.action_type, move.position, not is_player1)
                temp = self.alphabeta(game_copy, is_player1, player_1_stars,
                                      depth - 1, alpha, beta,
                                      not point_scored, move)
                if temp[1] < worse_score:
                    worse_move = move
                    worse_score = temp[1]
                beta = min(beta, worse_score)
                if beta <= alpha:
                    break
            return [worse_move, worse_score]


class E1_CPU(AlphaBetaCPU):

    def evaluate_goodness(self, game, is_player1, player_1_stars):
        """
        Evaluate the goodness of a board setting as the difference between a player and his enemy

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: A score representing how good the board setting is for a player
        """
        player1_score = len(np.argwhere(game.board_status == -4))
        player2_score = len(np.argwhere(game.board_status == +4))

        if is_player1:
            return player1_score - player2_score
        else:
            return player2_score - player1_score


class E2_CPU(AlphaBetaCPU):

    def __init__(self, max_depth=3, chain_points=1):
        self.MAX_DEPTH = max_depth
        self.CHAIN_POINTS = chain_points * (NUMBER_OF_DOTS - 1) * (NUMBER_OF_DOTS - 1)

    def evaluate_goodness(self, game, is_player1, player_1_stars):
        """
        Evaluate the goodness of a board setting as the difference between a player and his enemy, adding
        a price for building the correct number of long chains according to the long chain rule

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: A score representing how good the board setting is for a player
        """
        player1_score = len(np.argwhere(game.board_status == -4))
        player2_score = len(np.argwhere(game.board_status == +4))

        chain_points = 0

        long_chains = find_long_chains(game.board_status, game.row_status, game.col_status)
        number_of_long_chains = len(long_chains)

        if check_single_4(game.board_status):

            if NUMBER_OF_DOTS % 2 == 1:
                if (is_player1 and player_1_stars) or (not is_player1 and not player_1_stars):
                    if number_of_long_chains % 2 == 1:
                        chain_points = +self.CHAIN_POINTS
                else:
                    if number_of_long_chains % 2 == 0:
                        chain_points = +self.CHAIN_POINTS
            else:
                if (is_player1 and player_1_stars) or (not is_player1 and not player_1_stars):
                    if number_of_long_chains % 2 == 0:
                        chain_points = +self.CHAIN_POINTS

                else:
                    if number_of_long_chains % 2 == 1:
                        chain_points = +self.CHAIN_POINTS

        if is_player1:
            return player1_score - player2_score + chain_points
        else:
            return player2_score - player1_score + chain_points


class E3_CPU(AlphaBetaCPU):
    def evaluate_goodness(self, game, is_player1, player_1_stars):
        """
        Evaluate the goodness of a board setting as the difference between a player and his enemy, adding
        the predicted scores according to which chains the player and his enemy are going to conquer

        :param game: The Dot and Boxes match instance
        :param is_player1: Is the player1 the one making the move
        :param player_1_stars: Is the player1 the one making the first move
        :return: A score representing how good the board setting is for a player
        """
        player1_score = len(np.argwhere(game.board_status == -4))
        player2_score = len(np.argwhere(game.board_status == +4))

        chain_points = 0

        chains = sorted(find_chains(game.board_status, game.row_status, game.col_status), key=len)
        even_points = sum(len(even_chain) for even_chain in chains[::2])
        odd_points = sum(len(odd_chain) for odd_chain in chains[1::2])

        if game.is_end_game() and check_no_4(game.board_status):
            if (is_player1 and player_1_stars) or (not is_player1 and not player_1_stars):
                chain_points = +odd_points - even_points
            else:
                chain_points = -odd_points + even_points

        if is_player1:
            return player1_score - player2_score + chain_points
        else:
            return player2_score - player1_score + chain_points


class Dots_and_Boxes:

    def __init__(self, cpu1: Optional[CPU] = None, cpu2: Optional[CPU] = None, play=True, already_marked_boxes=None,
                 reset_board=None, player1_turn=None, pointsScored=None, col_status=None, row_status=None,
                 board_status=None, turntext_handle=None):
        self.start = None
        self.already_marked_boxes = already_marked_boxes
        self.reset_board = reset_board
        self.player1_turn = player1_turn
        self.pointsScored = pointsScored
        self.col_status = col_status
        self.row_status = row_status
        self.board_status = board_status
        self.turntext_handle = turntext_handle
        self.player1_starts = True

        if play:
            self.window = Tk()
            self.window.title('Dots_and_Boxes')
            self.canvas = Canvas(self.window, width=BOARD_SIZE, height=BOARD_SIZE)
            self.canvas.pack()
            self.refresh_board()

        self.cpu1 = cpu1
        self.cpu2 = cpu2
        if play:
            self.play_again()

    def get_copy(self):
        return Dots_and_Boxes(deepcopy(self.cpu1), deepcopy(self.cpu2), False, deepcopy(self.already_marked_boxes),
                              deepcopy(self.reset_board), deepcopy(self.player1_turn), deepcopy(self.pointsScored),
                              deepcopy(self.col_status), deepcopy(self.row_status), deepcopy(self.board_status),
                              deepcopy(self.turntext_handle))

    def get_game_state(self):
        return GameState(
            self.board_status.copy(),
            self.row_status.copy(),
            self.col_status.copy(),
            self.player1_turn)

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS - 1))
        self.row_status = np.zeros(shape=(NUMBER_OF_DOTS, NUMBER_OF_DOTS - 1))
        self.col_status = np.zeros(shape=(NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS))
        self.pointsScored = False

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

        self.turn()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        x = logical_position[0]
        y = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[y][x] == 0:
            occupied = False
        if type == 'col' and self.col_status[y][x] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - DOTS_DISTANCE / 4) // (DOTS_DISTANCE / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            x = int((position[0] - 1) // 2)
            y = int(position[1] // 2)
            logical_position = [x, y]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            y = int((position[1] - 1) // 2)
            x = int(position[0] // 2)
            logical_position = [x, y]
            type = 'col'

        return logical_position, type

    def pointScored(self):
        self.pointsScored = True

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = P1_COLOR_LM
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = P2_COLOR_LM
                self.shade_box(box, color)

    def update_board(self, type, logical_position, player1_turn):
        x = logical_position[0]
        y = logical_position[1]
        val = 1
        playerModifier = 1
        if player1_turn:
            playerModifier = -1

        if y < (NUMBER_OF_DOTS - 1) and x < (NUMBER_OF_DOTS - 1):
            self.board_status[y][x] = (abs(self.board_status[y][x]) + val) * playerModifier
            if abs(self.board_status[y][x]) == 4:
                self.pointScored()

        if type == 'row':
            self.row_status[y][x] = 1
            if y >= 1:
                self.board_status[y - 1][x] = (abs(self.board_status[y - 1][x]) + val) * playerModifier
                if abs(self.board_status[y - 1][x]) == 4:
                    self.pointScored()

        elif type == 'col':
            self.col_status[y][x] = 1
            if x >= 1:
                self.board_status[y][x - 1] = (abs(self.board_status[y][x - 1]) + val) * playerModifier
                if abs(self.board_status[y][x - 1]) == 4:
                    self.pointScored()

        return self.pointsScored

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = DOTS_DISTANCE / 2 + logical_position[0] * DOTS_DISTANCE
            end_x = start_x + DOTS_DISTANCE
            start_y = DOTS_DISTANCE / 2 + logical_position[1] * DOTS_DISTANCE
            end_y = start_y
        elif type == 'col':
            start_y = DOTS_DISTANCE / 2 + logical_position[1] * DOTS_DISTANCE
            end_y = start_y + DOTS_DISTANCE
            start_x = DOTS_DISTANCE / 2 + logical_position[0] * DOTS_DISTANCE
            end_x = start_x

        if self.player1_turn:
            color = P1_COLOR
        else:
            color = P2_COLOR
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=EDGE_WIDTH)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Player 1 wins'
            print(1)
            color = P1_COLOR
        elif player2_score > player1_score:
            text = 'Player 2 wins'
            print(2)
            color = P2_COLOR
        else:
            text = 'Its a tie'
            print('X')
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(BOARD_SIZE / 2, BOARD_SIZE / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(BOARD_SIZE / 2, 5 * BOARD_SIZE / 8, font="cmr 40 bold", fill=COLOR_GREEN,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(BOARD_SIZE / 2, 3 * BOARD_SIZE / 4, font="cmr 30 bold", fill=COLOR_GREEN,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(BOARD_SIZE / 2, 15 * BOARD_SIZE / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(NUMBER_OF_DOTS):
            x = i * DOTS_DISTANCE + DOTS_DISTANCE / 2
            self.canvas.create_line(x, DOTS_DISTANCE / 2, x,
                                    BOARD_SIZE - DOTS_DISTANCE / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(DOTS_DISTANCE / 2, x,
                                    BOARD_SIZE - DOTS_DISTANCE / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(NUMBER_OF_DOTS):
            for j in range(NUMBER_OF_DOTS):
                start_x = i * DOTS_DISTANCE + DOTS_DISTANCE / 2
                end_x = j * DOTS_DISTANCE + DOTS_DISTANCE / 2
                self.canvas.create_oval(start_x - DOT_WIDTH / 2, end_x - DOT_WIDTH / 2, start_x + DOT_WIDTH / 2,
                                        end_x + DOT_WIDTH / 2, fill=DOT_COLOR,
                                        outline=DOT_COLOR)

    def shade_box(self, box, color):
        start_x = DOTS_DISTANCE / 2 + box[1] * DOTS_DISTANCE + EDGE_WIDTH / 2
        start_y = DOTS_DISTANCE / 2 + box[0] * DOTS_DISTANCE + EDGE_WIDTH / 2
        end_x = start_x + DOTS_DISTANCE - EDGE_WIDTH
        end_y = start_y + DOTS_DISTANCE - EDGE_WIDTH
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def is_end_game(self):
        game = self
        for i in range(0, len(game.board_status), 1):
            for j in range(0, len(game.board_status), 1):
                if game.board_status[i][j] == 0:
                    return False
                if abs(game.board_status[i][j]) == 2 or abs(game.board_status[i][j]) == 4 or (
                        (abs(game.board_status[i][j] == 1) or abs(game.board_status[i][j] == 0)) and (
                        i < NUMBER_OF_DOTS - 2 and abs(game.board_status[i + 1][j]) == 2) or (
                                i > 0 and abs(game.board_status[i - 1][j]) == 2) or (
                                j < NUMBER_OF_DOTS - 2 and abs(game.board_status[i][j + 1]) == 2) or (
                                j > 0 and abs(game.board_status[i][j - 1]) == 2)):
                    pass
                else:
                    return False
        return True

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = P1_COLOR
        else:
            text += 'Player2'
            color = P2_COLOR

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(BOARD_SIZE - 5 * len(text),
                                                       BOARD_SIZE - DOTS_DISTANCE / 8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            self.update(valid_input, logical_position)
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def update(self, valid_input, logical_position):
        if valid_input and not self.is_grid_occupied(logical_position, valid_input):

            self.window.unbind(LEFT_CLICK)
            self.update_board(valid_input, logical_position, self.player1_turn)
            self.make_edge(valid_input, logical_position)
            self.mark_box()
            self.refresh_board()
            self.player1_turn = (not self.player1_turn) if not self.pointsScored else self.player1_turn
            self.pointsScored = False

            if self.is_gameover():
                self.display_gameover()
                self.window.bind(LEFT_CLICK, self.click)
                if loop:
                    self.play_again()
            else:
                self.display_turn_text()
                self.turn()

    def turn(self):
        self.start = time.time()
        current_cpu = self.cpu1 if self.player1_turn else self.cpu2
        if current_cpu is None:
            self.window.bind(LEFT_CLICK, self.click)
        else:
            self.window.after(CPU_DELAY_MS, self.cpu_turn, current_cpu)

    def cpu_turn(self, cpu: CPU):
        is_player1 = (cpu == self.cpu1)
        action = cpu.get_action(self, is_player1, self.player1_starts)
        self.update(action.action_type, action.position)