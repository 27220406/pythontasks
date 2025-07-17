import tkinter as tk
from tkinter import messagebox
import random

current_player = 'X'
board = [""] * 9
buttons = []

root = tk.Tk()
root.title("Tic Tac Toe")

def print_board():
    for i in range(9):
        buttons[i]["text"] = board[i]

def win(player):
    winning_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in winning_conditions:
        if all(board[i] == player for i in combo):
            return True
    return False

def disable_all_buttons():
    for btn in buttons:
        btn["state"] = "disabled"

def reset_game():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    for btn in buttons:
        btn.config(text="", state="normal")

def auto_move():
    empty_indexes = [i for i in range(9) if board[i] == ""]
    if empty_indexes:
        random_index = random.choice(empty_indexes)
        board[random_index] = 'O'
        buttons[random_index]["text"] = 'O'
        buttons[random_index]["state"] = "disabled"
        if win('O'):
            messagebox.showinfo("Game Over", "🤖 Player O (AI) wins!")
            disable_all_buttons()
        elif "" not in board:
            messagebox.showinfo("Game Over", "It's a draw!")

def on_click(index):
    global current_player
    if board[index] == "" and current_player == 'X':
        board[index] = 'X'
        print_board()
        buttons[index]["state"] = "disabled"
        if win('X'):
            messagebox.showinfo("Game Over", "🎉 Player X wins!")
            disable_all_buttons()
            return
        elif "" not in board:
            messagebox.showinfo("Game Over", "It's a draw!")
            return
        current_player = 'O'
        root.after(500, auto_turn)  # Give a slight delay before AI moves

def auto_turn():
    global current_player
    auto_move()
    if not win('O') and "" in board:
        current_player = 'X'

# UI setup
for i in range(9):
    btn = tk.Button(root, text="", font=('Helvetica', 20), height=3, width=6,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)

reset_button = tk.Button(root, text="Reset Game", font=('Helvetica', 12), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
