from random import randrange

def display_board(board):
    print(r'+-------+-------+-------+')
    print(r'|       |       |       |')
    print(r'|   {}   |   {}   |   {}   |'.format(board[0][0], board[0][1], board[0][2]))
    print(r'|       |       |       |')
    print(r'+-------+-------+-------+')
    print(r'|       |       |       |')
    print(r'|   {}   |   {}   |   {}   |'.format(board[1][0], board[1][1], board[1][2]))
    print(r'|       |       |       |')
    print(r'+-------+-------+-------+')
    print(r'|       |       |       |')
    print(r'|   {}   |   {}   |   {}   |'.format(board[2][0], board[2][1], board[2][2]))
    print(r'|       |       |       |')
    print(r'+-------+-------+-------+')


def enter_move(board, game_board):
    r = 0
    while True:
        move = int(input('Wykonaj swój ruch: '))
        if (move in game_board[0]):
            r = 0
            break
        elif (move in game_board[1]):
            r = 1
            break
        elif (move in game_board[2]):
            r = 2
            break
        else:
            print('To pole już zajęte lub nie istnieje. Spróbuj jeszcze raz!')
    game_board[r][game_board[r].index(move)] = 'O'
    display_board(game_board)


def make_list_of_free_fields(board):
    res = []
    for row in range(3):
        for col in range(3):
            if str(board[row][col]).isdigit():
                res.append((row, col))
    return res


def victory_for(board, sign):
    if (board[0][0] == sign and board[1][1] == sign and board[2][2] == sign) or \
      (board[0][2] == sign and board[1][1] == sign and board[2][0] == sign) or \
      (board[0].count(sign) == 3) or \
      (board[1].count(sign) == 3) or \
      (board[2].count(sign) == 3) or \
      (board[0][0] == sign and board[1][0] == sign and board[2][0] == sign) or \
      (board[0][1] == sign and board[1][1] == sign and board[2][1] == sign) or \
      (board[0][2] == sign and board[1][2] == sign and board[2][2] == sign):
        if sign == 'O':
            print('Wygrałeś!')
        else:
            print('Wygrał komputer!')
        return True
    else:
        return False


def draw_move(board, game_board):
    if len(board) == 9:
        game_board[1][1] = 'X'
    else:
        move = randrange(len(board))
        game_board[board[move][0]][board[move][1]] = 'X'
    display_board(game_board)


def main():
    game_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    draw_move(make_list_of_free_fields(game_board), game_board)
    sign = 'O'
    while True:
        if victory_for(game_board, 'X') or victory_for(game_board, 'O'):
            break
        else:
            free_fields = make_list_of_free_fields(game_board)
            if len(free_fields) == 0:
                print('Remis')
                break
            elif sign == 'O':
                enter_move(free_fields, game_board)
                sign = 'X'
            else:
                draw_move(free_fields, game_board)
                sign = 'O'


main()
