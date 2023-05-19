import pygame
import sys
import math
import time
import random

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