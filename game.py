import pygame as pygame
from board import Board
from AI_Agent import AI_agent
import time
import random
import math


# GAME LINK
# http://kevinshannon.com/connect4/

def main():
    board = Board()
    ai_agent = AI_agent()
    time.sleep(2)

    mohsen =True
    game_end = False
    while not game_end:
        game_board, game_end = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)
        print("-------------------------------------------------------------------------------")
        col, score = alphaBeta(game_board, 6, -math.inf, math.inf, True)
        # if mohsen:
        #     col = random.randint(0, 6)
        #     mohsen =False
        print(col)
        board.select_column(col)
        time.sleep(2)
        board.print_grid(game_board)
        
main()
