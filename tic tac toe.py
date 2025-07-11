board = [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']

def print_board():
    print("\n")
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("---|---|---")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("---|---|---")
    print(f"{board[6]}|{board[7]}|{board[8]}")
    print("   |   |")
    print("\n")

def win(board, player):
    winning_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_conditions:
        if all(board[i] == f' {player} ' for i in combo):
            return True
    return False

current_player = 'X'

for i in range(9):
    print_board()

    move = int(input(f"Player {current_player}, choose your move (1-9): ")) - 1

    if board[move] in [' X ', ' O ']:
        print("This spot is already taken. Try again!")
        continue

    board[move] = f' {current_player} '

    if win(board, current_player):
        print_board()
        print(f" Player {current_player} wins!")
        break

    current_player = 'O' if current_player == 'X' else 'X'
else:
    print_board()
    print("It's a draw!")
