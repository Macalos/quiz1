board = ["  " for i in range(9)]

def pr_board():
    row1 = "| {} | {} | {} |".format(board[0], board[1], board[2])
    row2 = "| {} | {} | {} |".format(board[3], board[4], board[5])
    row3 = "| {} | {} | {} |".format(board[6], board[7], board[8])

    print()
    print(row1)
    print(row2)
    print(row3)
    print()


def player(icon):
    if icon == "X":
        print("X's turn")
        

    elif icon == "O":        
        print("O's turn")
        

    choice = int(input("Enter your move (1-9): "))

    if choice > 9 or choice < 1:
        print()
        print("OUT OF RANGE!")
        return 

    if board[choice - 1] == "  ":
        board[choice - 1] = icon
    else:
        print()
        print("SPACE ALREADY TAKEN!")

           

def victory(icon):
    if (board[0] == board[1] == board[2] == icon) or \
       (board[3] == board[4] == board[5] == icon) or \
       (board[6] == board[7] == board[8] == icon) or \
       (board[0] == board[3] == board[6] == icon) or \
       (board[1] == board[4] == board[7] == icon) or \
       (board[2] == board[5] == board[8] == icon) or \
       (board[0] == board[4] == board[8] == icon) or \
       (board[2] == board[4] == board[6] == icon):
        return True
    else:
        return False

def draw():        
    if "  " not in board:
        return True
    else:
        return False


while True:
    pr_board()
    player("X")
    pr_board()
    if victory("X"):
        print("X wins!")
        break
    elif draw():
        print("Draw!")
        break
    
    player("O")
    if victory("O"):
        pr_board()
        print("O wins!")
        break
    elif draw():
        print("Draw!")
        break
