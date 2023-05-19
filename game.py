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
        col, score = ai_agent.minimax(game_board, 4, True)
        # if mohsen:
        #     col = random.randint(0, 6)
        #     mohsen =False
        print(col)
        board.select_column(col)
        time.sleep(2)
        board.print_grid(game_board)
        
main()
