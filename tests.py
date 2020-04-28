import random
from beautifultable import BeautifulTable

main_list = ['' for _ in range(0, 9)]


def display_board(board):
    table = BeautifulTable()
    table.append_row(main_list[:3])
    table.append_row(main_list[3:6])
    table.append_row(main_list[6:])
    table.set_padding_widths(3)
    table.set_style(BeautifulTable.STYLE_BOX_DOUBLED)

    print(table)

def player_input():
    while True:
        xo = input("choose your character(X or O): ")
        if xo == 'X' or xo == 'O':
            return xo
        else:
            print("Invalid input!")


def place_marker(board, marker, position):
    if position >= 10 or position <= 0:
        print("Out of range!")
    board[position - 1] = marker


def win_check(board, mark):
    return ((board[6] == mark and board[7] == mark and board[8] == mark)
            or  # across the top
            (board[3] == mark and board[4] == mark
             and board[5] == mark) or  # across the middle
            (board[0] == mark and board[1] == mark and board[2] == mark)
            or  # across the bottom
            (board[6] == mark and board[3] == mark
             and board[0] == mark) or  # down the middle
            (board[7] == mark and board[4] == mark and board[1] == mark)
            or  # down the middle
            (board[8] == mark and board[5] == mark
             and board[2] == mark) or  # down the right side
            (board[6] == mark and board[4] == mark and board[2] == mark)
            or  # diagonal
            (board[8] == mark and board[4] == mark and board[0] == mark)
            )  # diagonal


def choose_first():
    return random.randint(1, 2)

def space_check(board, position):
    if board[position] == 'X' or board[position] == 'O':
        return False
    else:
        return True


def clear_board(board):
    board = list(map(lambda x: '', board))
    return board


def full_board_check(board):
    for i in board:
        if i == '':
            return False


def player_choice(board):
    while True:
        pnum = int(input("Your turn(1-9):"))
        if (space_check(board, pnum - 1)):
            return pnum
        else:
            print("that's not free...")


def replay():
    return input("Do you likes to play again(T or F)?")

# place_marker, win_check, space_check, full_board_check, player_choice, replay
print('Welcome to Tic Tac Toe!')
prepare_game = True
while prepare_game:
    game_on = True
    marker_one = player_input()
    if marker_one == 'X':
        marker_two = 'O'
    else:
        marker_two = 'X'
    print(f'Player 1 is {marker_one}, Player 2 is {marker_two}')
    pl_turn = choose_first()
    print(f'Player {pl_turn} first')
    display_board(main_list)
    while game_on:
        position = player_choice(main_list)
        if pl_turn == 1:
            marker = marker_one
            pl_turn = 2
        else:
            marker = marker_two
            pl_turn = 1
        place_marker(main_list, marker, position)
        display_board(main_list)
        if win_check(main_list, marker):
            if pl_turn == 1:
                pl_turn = 2
            else:
                pl_turn = 1
            print(f'Player{pl_turn} wins!')
            main_list = clear_board(main_list)
            # main_list = list(map(lambda x : '', main_list))
            if replay() == 'T':
                game_on = False
            else:
                game_on = False
                prepare_game = False
        if full_board_check(main_list):
            print("There's no space!")
            main_list = list(map(lambda x : '', main_list))
            game_on = False
            if replay() == 'F':
                prepare_game = False
