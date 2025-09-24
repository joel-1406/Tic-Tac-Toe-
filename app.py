import tkinter as tk
from tkinter import messagebox
import random

# -------------------------------
# Game Setup
# -------------------------------
root = tk.Tk()
root.title("🎮 Tic Tac Toe - Unbeatable AI")
root.resizable(False, False)

player = "X"
computer = "O"
buttons = [[None, None, None] for _ in range(3)]
score_player = 0
score_computer = 0

# -------------------------------
# Functions
# -------------------------------
def check_winner(board):
    """Return winner if found, else None"""
    # Rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            return board[row][0]
    # Cols
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    # Diags
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def is_draw(board):
    """Check if board is full"""
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True

def minimax(board, depth, is_max):
    """AI logic using minimax"""
    winner = check_winner(board)
    if winner == computer:
        return 10 - depth
    elif winner == player:
        return depth - 10
    elif is_draw(board):
        return 0

    if is_max:
        best = -1000
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = computer
                    best = max(best, minimax(board, depth+1, False))
                    board[r][c] = ""
        return best
    else:
        best = 1000
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = player
                    best = min(best, minimax(board, depth+1, True))
                    board[r][c] = ""
        return best

def best_move():
    """Find best move for computer"""
    best_val = -1000
    move = None
    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == "":
                buttons[r][c]["text"] = computer
                board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
                move_val = minimax(board, 0, False)
                buttons[r][c]["text"] = ""
                if move_val > best_val:
                    best_val = move_val
                    move = (r, c)
    return move

def player_move(r, c):
    if buttons[r][c]["text"] == "":
        buttons[r][c]["text"] = player
        buttons[r][c].config(bg="lightgreen")
        board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
        if check_winner(board):
            end_game(player)
            return
        elif is_draw(board):
            end_game(None)
            return
        comp_r, comp_c = best_move()
        buttons[comp_r][comp_c]["text"] = computer
        buttons[comp_r][comp_c].config(bg="lightcoral")
        board = [[buttons[i][j]["text"] for j in range(3)] for i in range(3)]
        if check_winner(board):
            end_game(computer)
        elif is_draw(board):
            end_game(None)

def end_game(winner):
    global score_player, score_computer
    if winner == player:
        score_player += 1
        messagebox.showinfo("Game Over", "🎉 You Win!")
    elif winner == computer:
        score_computer += 1
        messagebox.showinfo("Game Over", "💻 Computer Wins!")
    else:
        messagebox.showinfo("Game Over", "It's a Draw!")
    update_score()
    reset_board()

def reset_board():
    for r in range(3):
        for c in range(3):
            buttons[r][c]["text"] = ""
            buttons[r][c].config(bg="lightyellow")

def restart_all():
    global score_player, score_computer
    score_player, score_computer = 0, 0
    update_score()
    reset_board()

def update_score():
    score_label.config(text=f"Score - You: {score_player} | Computer: {score_computer}")

# -------------------------------
# GUI Layout
# -------------------------------
title = tk.Label(root, text="🎮 Tic Tac Toe (Unbeatable AI)", font=("Arial", 18, "bold"), fg="white", bg="purple", pady=10)
title.grid(row=0, column=0, columnspan=3, sticky="we")

score_label = tk.Label(root, text="Score - You: 0 | Computer: 0", font=("Arial", 12), bg="black", fg="white")
score_label.grid(row=1, column=0, columnspan=3, sticky="we")

for r in range(3):
    for c in range(3):
        buttons[r][c] = tk.Button(root, text="", font=("Arial", 24, "bold"), width=5, height=2, bg="lightyellow",
                                  command=lambda r=r, c=c: player_move(r, c))
        buttons[r][c].grid(row=r+2, column=c, padx=5, pady=5)

reset_btn = tk.Button(root, text="Reset Board", font=("Arial", 12), command=reset_board, bg="lightblue")
reset_btn.grid(row=5, column=0, pady=10)

restart_btn = tk.Button(root, text="Restart Game", font=("Arial", 12), command=restart_all, bg="orange")
restart_btn.grid(row=5, column=2, pady=10)

root.configure(bg="gray20")
root.mainloop()
