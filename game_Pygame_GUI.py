import pygame
import sys
import numpy as np
import math
import time
import random
from copy import deepcopy
from board import Board
from AI_Agent import AI_agent

board = Board()
ai_agent = AI_agent()

squareSize = 100
radius = int(squareSize/2 -5)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# define the players
AGENT = 2
COMPUTER = 1
EMPTY = 0
COLUMN_COUNT = 7
ROW_COUNT = 6
WINDOW_LENGTH = 4


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT), int)
	return board
              
def betaAlpha(board, depth, alpha, beta, isMaximizing):
    valid_locations = ai_agent.get_valid_moves(board)
    is_terminal = ai_agent.is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if ai_agent.is_winner(board, AGENT):
                return (None, 100000000000000)
            elif ai_agent.is_winner(board, COMPUTER):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, ai_agent.score_position(board, COMPUTER))
    if isMaximizing:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            ai_agent.make_move(b_copy, col, AGENT)
            new_score = betaAlpha(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            ai_agent.make_move(b_copy, col, COMPUTER)
            new_score = betaAlpha(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, YELLOW, (c*squareSize, r*squareSize + squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, BLACK, (int(c*squareSize + squareSize/2),  int(r*squareSize + squareSize + squareSize/2)), radius)
            

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if(board[r][c] == 2):
                pygame.draw.circle(screen, RED, (int(c*squareSize + squareSize/2),  int((r+1)*squareSize + squareSize/2)), radius)
            elif(board[r][c] == 1):
                pygame.draw.circle(screen, BLUE, (int(c*squareSize + squareSize/2),  int((r+1)*squareSize + squareSize/2)), radius)
    pygame.display.update()

pygame.init()

width = COLUMN_COUNT * squareSize
height = (ROW_COUNT + 1) * squareSize
size = (width, height)
screen = pygame.display.set_mode(size)
board = create_board()

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
game_over = False

turn = random.randint(COMPUTER, AGENT)
move = random.choice(ai_agent.get_valid_moves(board))
pygame.time.wait(500)
ai_agent.make_move(board, move, turn)
draw_board(board)
if turn == AGENT:
     turn -= 1
else:
     turn += 1
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if turn == AGENT:
        col, minimax_score = betaAlpha(board, 5, -math.inf, math.inf, True)
        pygame.time.wait(500)
        ai_agent.make_move(board, col, AGENT)
        if ai_agent.is_winner(board, AGENT):
            label = myfont.render("Player1 wins!!", 1, RED)
            screen.blit(label, (30,10))
            game_over = True
        turn -= 1
        print(board)
        draw_board(board)

    if len(ai_agent.get_valid_moves(board)) == 0:
        label = myfont.render("TIE!!", 1, YELLOW)
        screen.blit(label, (30,10))
        game_over = True

	# # Ask for Player 2 Input
    if turn == COMPUTER and not game_over:				

        col, minimax_score = ai_agent.alphaBeta(board, 5, -math.inf, math.inf, True)

        pygame.time.wait(500)
        ai_agent.make_move(board, col, COMPUTER)

        if ai_agent.is_winner(board, COMPUTER):
            label = myfont.render("Player2 wins!!", 1, BLUE)
            screen.blit(label, (30,10))
            game_over = True

        turn += 1
        print(board)
        draw_board(board)
        
        if len(ai_agent.get_valid_moves(board)) == 0:
            label = myfont.render("TIE!!", 1, YELLOW)
            screen.blit(label, (30,10))
            game_over = True

pygame.time.wait(3000)