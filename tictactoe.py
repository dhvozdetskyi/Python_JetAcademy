import random
import copy

field_coord = {"0": [1, 1], "1": [1, 2], "2": [1, 3], "3": [2, 1], "4": [2, 2], "5": [2, 3], "6": [3, 1], "7": [3, 2], "8": [3, 3]}


def checkwin(s, symbol):
    if ((s[0] == s[1] == s[2] == symbol) or (s[3] == s[4] == s[5] == symbol) or (s[6] == s[7] == s[8] == symbol) or
       (s[0] == s[3] == s[6] == symbol) or (s[1] == s[4] == s[7] == symbol) or (s[2] == s[5] == s[8] == symbol) or
       (s[0] == s[4] == s[8] == symbol) or (s[6] == s[4] == s[2] == symbol)):
        return True
    else:
        return False


def drawfield(s):
    print("---------")
    print(f'| {s[0]} {s[1]} {s[2]} |')
    print(f'| {s[3]} {s[4]} {s[5]} |')
    print(f'| {s[6]} {s[7]} {s[8]} |')
    print("---------")


def checkisempty(s, cell):
    for k in field_coord:
        if field_coord[k] == cell:
            if s[int(k)] in ('_', ' '):
                return True
            else:
                return False
            break

def setplace(s, cell, symbol):
    for k in field_coord:
        if field_coord[k] == cell:
            s[int(k)] = symbol
            break
    return s

class User:
    def __init__(self, name):
        self.name = name

    def selectcoords(self, s, symbol):
        while True:
            coord = input("Enter the coordinates: ").strip()
            if ' ' in coord:
                row, col = coord.split()
                if not (row.isdigit() and col.isdigit()):
                    print("You should enter numbers!")
                elif (int(row) > 3) or (int(row) < 1) or (int(col) > 3) or (int(col) < 1):
                    print("Coordinates should be from 1 to 3!")
                elif not checkisempty(s, [int(row), int(col)]):
                    print("This cell is occupied! Choose another one!")
                else:
                    break
            else:
                print("You should enter numbers!")
                continue
        return row, col


class EasyLevel:
    def __init__(self, name):
        self.name = name

    def randomcoords(self):
        return random.randint(1, 3), random.randint(1, 3)

    def selectcoords(self, s, symbol):
        row, col = self.randomcoords()
        while True:
            if checkisempty(s, [row, col]):
                break
            else:
                row, col = self.randomcoords()
        return row, col

class MediumLevel(EasyLevel):

    def getemptycells(self, s):
        return [field_coord[str(k)] for k in range(0, 9) if s[k] == ' ']


    def selectcoords(self, s, symbol):
        if symbol == 'X':
            enemy = 'O'
        else:
            enemy = 'X'

        emptycells = self.getemptycells(s)
        if len(emptycells) == 1:
            return emptycells[0][0], emptycells[0][1]
        else:
            for c in emptycells:
                s1, s2 = copy.copy(s), copy.copy(s)
                s1 = setplace(s1, c, symbol)
                s2 = setplace(s2, c, enemy)
                if checkwin(s1, symbol) or checkwin(s2, enemy):
                    return c[0], c[1]
            else:
                cell = random.randint(0, len(emptycells) - 1)
                return emptycells[cell][0], emptycells[cell][1]


class HardLevel(MediumLevel):

    def minimax(self, board, p):
        self.fc += 1
        emptycells = self.getemptycells(board)
        if checkwin(board, p):
            return {'score':10}
        elif checkwin(board, self.enemy):
            return {'score':-10}
        elif len(emptycells) == 0:
            return {'score':0}
        else:
            moves = []
            for i in range(0, len(emptycells)):
                move = {}
                for f in field_coord:
                    if field_coord[f] == emptycells[i]:
                        move['index'] = f
                setplace(board, emptycells[i], p)
                if p == self.symbol:
                    result = self.minimax(board, self.enemy)
                else:
                    result = self.minimax(board, self.symbol)
                move['score'] = result['score']

                setplace(board, emptycells[i], ' ')
                moves.append(move)

            bestMove = None
            if (p == self.symbol):
                bestScore = -10000;
                for i in range(0, len(moves)):
                    if (moves[i]['score'] > bestScore):
                        bestScore = moves[i]['score']
                        bestMove = i
            else:
                bestScore = 10000;
                for i in range(0, len(moves)):
                    if (moves[i]['score'] < bestScore):
                        bestScore = moves[i]['score']
                        bestMove = i

            return moves[bestMove]

    def selectcoords(self, s, symbol):
        if symbol == 'X':
            self.enemy = 'O'
        else:
            self.enemy = 'X'
        self.symbol = symbol
        self.fc = 0
        board = copy.copy(s)
        pos = self.minimax(board, symbol)
        return field_coord[str(pos['index'])]

class Player:
    def __init__(self, symbol, level):
        self.symbol = symbol
        if level == 'easy':
            self.level = EasyLevel(level)
        elif level == 'medium':
            self.level = MediumLevel(level)
        elif level == 'hard':
            self.level = HardLevel(level)
        elif level == 'user':
            self.level = User(level)


    def selectcoordandsetplace(self, s):
        if self.level.name != 'user':
            print('Making move level "{}"'.format(self.level.name))
        row, col = self.level.selectcoords(s, self.symbol)
        return setplace(s, [int(row), int(col)], self.symbol)  # set move


while True:  # main program loop
    command = input('Input command: ')
    if command == 'exit':
        break
    elif command.count(' ') != 2:
        print('Bad parameters!')
        continue
    else:
        cmd, p1, p2 = command.split()
        player1 = Player('X', p1)
        player2 = Player('O', p2)

    s = list('         ')
    drawfield(s)
    current_player = player1
    while True:  # main game loop
        s = current_player.selectcoordandsetplace(s)
        drawfield(s)  # print field after move
        if checkwin(s, 'X'):
            print('X wins')
            break
        elif checkwin(s, 'O'):
            print('O wins')
            break
        elif s.count(' ') == 0:
            print('Draw')
            break

        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
