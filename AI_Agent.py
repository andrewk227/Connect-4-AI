import pygame
import sys
import math
import time
import random
from copy import deepcopy
from board import Board as br

# define the player
AGENT = 1
EMPTY = 0
COMPUTER = 2
COLUMNS = 7
ROWS = 6
WINDOW_LENGTH = 4


class AI_agent:

    # function to get the valid moves in the current state of the board
    def get_valid_moves(self, board):
        valid_locations = []
        for col in range(COLUMNS):
            if board[0][col] == 0:
                valid_locations.append(col)
        return valid_locations

    # function to put the piece in the board
    def make_move(self, board, col, player):
        for r in range(5, -1, -1):
            if board[r][col] == 0:
                board[r][col] = player
                return
            
    # function to get the move evaluation
    def evaluate_window(self, window, player):
        score = 0
        opponent = COMPUTER if player == AGENT else AGENT
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(EMPTY) == 2:
            score += 2
        elif window.count(opponent) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, player):
        score = 0
        # Score center column
        center_array = []
        for row in board:
            for i in row:
                if  len(row) > 3:
                    center_array.append(int(row[3]))
        center_count = center_array.count(player)
        score += center_count * 3

        ## Score Horizontal
        for row in range(6):
            row_array = []
            for col in range(7):
              for i in range(4):
                  window = row_array[i:i + 4]
                  score += self.evaluate_window(window, player)

        # Score Vertical
        for col in range(7):
            col_array = []
            for row in range(6):
                col_array.append(int(board[row][col]))
            for i in range(3, 6):
                window = col_array[i:i - 4:-1]  # Reverse the window to start from the bottom
                score += self.evaluate_window(window, player)

        ## Score posiive sloped diagonal
        for row in range(3):
            for col in range(4):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        for row in range(3):
            for col in range(4):
                window = [board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score
    
    def is_winner(self, board, player):
        # check rows
        for row in range(6):
            for col in range(4):
                if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                    return True

        # check columns
        for row in range(3):
            for col in range(7):
                if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                    return True

        # check diagonal (down-right)
        for row in range(3):
            for col in range(4):
                if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][
                    col + 2] == player and board[row + 3][col + 3] == player:
                    return True

        # check diagonal (up-right)
        for row in range(3, 6):
            for col in range(4):
                if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][
                    col + 2] == player and board[row - 3][col + 3] == player:
                    return True

    def is_terminal_node(self, board):
        return (self.is_winner(board, AGENT) or self.is_winner(board, COMPUTER) or len(self.get_valid_moves(board)) == 0)

    # function to get the best move using Minimax algorithm
    def minimax(self, board, depth, isMaximizing):
        valid_locations = self.get_valid_moves(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_winner(board, AGENT):
                    return (None, 100000000000000)
                elif self.is_winner(board, COMPUTER):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, AGENT))

        if isMaximizing:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                board_copy = deepcopy(board)
                self.make_move(board_copy, col, AGENT)
                new_score = self.minimax(board_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                board_copy = deepcopy(board)
                self.make_move(board_copy, col, COMPUTER)
                new_score = self.minimax(board_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

    # function to get the best move using Minimax algorithm and alpha-beta pruning
    def alphaBeta(self, board, depth, alpha, beta, isMaximizing):
        valid_locations = self.get_valid_moves(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.is_winner(board, AGENT):
                    return (None, 100000000000000)
                elif self.is_winner(board, COMPUTER):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, AGENT))
            
        if isMaximizing:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                board_copy = deepcopy(board)
                self.make_move(board_copy, col, AGENT)
                new_score = self.alphaBeta(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                board_copy = deepcopy(board)
                self.make_move(board_copy, col, COMPUTER)
                new_score = self.alphaBeta(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value