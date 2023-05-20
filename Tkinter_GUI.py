import tkinter as tk
from board import Board
from AI_Agent import AI_agent
import time
import random
import math

board = Board()
ai_agent = AI_agent()

def start_game():
    algo = algorithm_var.get()
    level = difficulty_var.get()
    time.sleep(2)
    score = 0
    game_end = False
    while not game_end :
        game_board, game_end = board.get_game_grid()

        if algo == "Minimax":
            if level == "Easy":
                col, score = ai_agent.minimax(game_board, 2, True)
            elif level == "Medium":
                col, score = ai_agent.minimax(game_board, 3, True)
            elif level == "Hard":
                col, score = ai_agent.minimax(game_board, 4, True)

        elif algo == "Alpha-Beta Pruning":
            if level == "Easy":
                col, score = ai_agent.alphaBeta(game_board, 2, -math.inf, math.inf, True)
            elif level == "Medium":
                col, score = ai_agent.alphaBeta(game_board, 4, -math.inf, math.inf, True)
            elif level == "Hard":
                col, score = ai_agent.alphaBeta(game_board, 6, -math.inf, math.inf, True)
        board.select_column(col)
        print (game_end)
        print("Col: ", col, " score: ", score)
        time.sleep(2)
        print("-------------------------------------------------------------------------------")
        board.print_grid(game_board)
    
    print("hamok4a")

root = tk.Tk()
root.geometry("400x230")
root.title("Game Options")

algorithm_var = tk.StringVar()
algorithm_choices = ["Minimax", "Alpha-Beta Pruning"]
algorithm_menu = tk.OptionMenu(root, algorithm_var,* algorithm_choices)
algorithm_label = tk.Label(root, text="Select Algorithm Type", width=20)
algorithm_label.pack()
algorithm_menu.pack()

difficulty_var = tk.StringVar()
difficulty_choices = ["Easy", "Medium", "Hard"]
difficulty_menu = tk.OptionMenu(root, difficulty_var,*difficulty_choices)
difficulty_label = tk.Label(root, text="Select Difficulty Level", width=20)
difficulty_label.pack()
difficulty_menu.pack()

start_button = tk.Button(root, text="Start Game", command=start_game, width=20, height=1, padx=10, pady=15)
print(start_button)
start_button.pack()


root.mainloop()