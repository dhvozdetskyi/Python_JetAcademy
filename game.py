import numpy as np


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.field = np.full((row, col), '-')
        self.filledFields = None

    def draw(self, field):
        for i in range(field.shape[0]):
            print(*field[i])
        print()

    def setFilledFields(self, fields):
        self.filledFields = []
        for i in range(fields.shape[0]):
            for j in range(fields.shape[1]):
                if fields[i][j] == '0':
                    self.filledFields.append(i * 10 + j)

    def disappear(self, fields):
        self.setFilledFields(fields)
        d = {}
        for f in self.filledFields:
            for i in range(1, self.col + 1):
                if f < self.field.shape[1] * i:
                    if d.get(str(i - 1)):
                        d[str(i - 1)].append(f)
                    else:
                        d[str(i - 1)] = [f]
                    break
        fullrows = []
        for p in d:
            if len(d[p]) == self.col:
                fullrows.append(int(p))
        for row in fullrows:
            for f in self.filledFields[:]:
                if row * 10 <= f < (row + 1) * 10:
                    self.filledFields.remove(f)
            for i in range(len(self.filledFields)):
                if self.filledFields[i] < row * 10:
                    self.filledFields[i] += 10

        field = np.full((self.row, self.col), '-')
        if self.filledFields:
            for f in self.filledFields:
                if f < 10:
                    field[0][f] = '0'
                else:
                    field[f // 10][f % 10] = '0'

        self.draw(field)


class Figure:
    def __init__(self, board):
        self.board = board
        self.board_y = board.field.shape[0]
        self.board_x = board.field.shape[1]
        self.state = []
        self.field = np.full((1, 1), '-')
        self.current_state = None
        self.anchor = [0, board.field.shape[1] // 2 - 2]  # [row, col]
        self.prepare_empty_field()

    def setboard(self, board):
        self.board = board

    def prepare_empty_field(self):
        self.field = np.full((self.board_y, self.board_x), '-')
        if self.board.filledFields:
            for f in self.board.filledFields:
                if f < 10:
                    self.field[0][f] = '0'
                else:
                    self.field[f // 10][f % 10] = '0'

    def state0(self):
        self.current_state = 0

    def state90(self):
        self.current_state = 90

    def state180(self):
        self.current_state = 180

    def state270(self):
        self.current_state = 270

    def change_state(self):
        if self.current_state == 0:
            self.current_state = 90
        elif self.current_state == 90:
            self.current_state = 180
        elif self.current_state == 180:
            self.current_state = 270
        elif self.current_state == 270:
            self.current_state = 0

    def init_current_state(self):
        self.prepare_empty_field()
        if self.current_state == 0:
            self.state0()
        elif self.current_state == 90:
            self.state90()
        elif self.current_state == 180:
            self.state180()
        elif self.current_state == 270:
            self.state270()

    def down(self):
        tmpstate = []
        for a in self.state:
            tmpstate.append(a + 10)
        if (max(self.state) // 10 == self.board_y - 1) or (self.board.filledFields and any(np.intersect1d(self.board.filledFields, tmpstate, assume_unique=True))):
            return None
        self.anchor[0] += 10

    def shift_left(self):
        for a in self.state:
            if (a % 10 == 0) or (self.board.filledFields and any(np.intersect1d(self.board.filledFields, [a - 1]))):
                return None
        if self.anchor[1] % 10 == 0:
            self.anchor[1] += 9
        else:
            self.anchor[1] -= 1

    def shift_right(self):
        for a in self.state:
            if (a % 10 == 9) or (self.board.filledFields and any(np.intersect1d(self.board.filledFields, [a + 1]))):
                return None
        if self.anchor[1] % 10 == 9:
            self.anchor[1] -= 9
        else:
            self.anchor[1] += 1

    def draw_figure_on_board(self, space=True):
        self.init_current_state()
        for i in self.state:
            if i < 10:
                self.field[0][i] = '0'
            else:
                self.field[i // 10][i % 10] = '0'
        self.board.draw(self.field)


class ShapeI(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'I'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 30 + (self.anchor[1] + 1) % 10]

    def state90(self):
        super().state90()
        self.prepare_empty_field()
        self.state = [self.anchor[0] + self.anchor[1],
                      self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + (self.anchor[1] + 3) % 10]

    def state180(self):
        super().state180()
        self.state0()

    def state270(self):
        super().state270()
        self.state90()


class ShapeO(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'O'
        self.state0()

    def state0(self):
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10]
        super().state0()

    def state90(self):
        self.state0()
        super().state90()

    def state180(self):
        self.state0()
        super().state180()

    def state270(self):
        self.state0()
        super().state270()


class ShapeT(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'T'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10]

    def state90(self):
        super().state90()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + self.anchor[1] % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10]

    def state180(self):
        super().state180()
        self.state = [self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 2) % 10]

    def state270(self):
        super().state270()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + (self.anchor[1] + 3) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10]


class ShapeL(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'L'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 2) % 10]

    def state90(self):
        super().state90()
        self.state = [self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + self.anchor[1] % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10]

    def state180(self):
        super().state180()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 2) % 10]

    def state270(self):
        super().state270()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + (self.anchor[1] + 3) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10]


class ShapeS(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'S'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + self.anchor[1] % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10]

    def state90(self):
        super().state90()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 2) % 10]

    def state180(self):
        super().state180()
        self.state0()

    def state270(self):
        super().state270()
        self.state90()


class ShapeZ(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'Z'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 3) % 10]

    def state90(self):
        super().state90()
        self.state = [self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10]

    def state180(self):
        super().state180()
        self.state0()

    def state270(self):
        super().state270()
        self.state90()


class ShapeJ(Figure):
    def __init__(self, board):
        super().__init__(board)
        self.name = 'J'
        self.state0()

    def state0(self):
        super().state0()
        self.state = [self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 2) % 10]

    def state90(self):
        super().state90()
        self.state = [self.anchor[0] + self.anchor[1] % 10,
                      self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10]

    def state180(self):
        super().state180()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 20 + (self.anchor[1] + 1) % 10]

    def state270(self):
        super().state270()
        self.state = [self.anchor[0] + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 1) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 2) % 10,
                      self.anchor[0] + 10 + (self.anchor[1] + 3) % 10]


def get_shape(b, typ):
    if typ == 'T':
        return ShapeT(b)
    elif typ == 'O':
        return ShapeO(b)
    elif typ == 'S':
        return ShapeS(b)
    elif typ == 'L':
        return ShapeL(b)
    elif typ == 'J':
        return ShapeJ(b)
    elif typ == 'Z':
        return ShapeZ(b)
    else:
        return ShapeI(b)


def main():
    col, row = map(int, input().split(' '))
    input()
    typ = input().upper()
    b = Board(row, col)
    shape = get_shape(b, typ)

    b.draw(b.field)
    shape.draw_figure_on_board()
    while True:
        cmd = input()
        if cmd == 'exit':
            break
        if cmd == 'rotate':
            shape.change_state()
        elif cmd == 'left':
            shape.shift_left()
        elif cmd == 'right':
            shape.shift_right()
        elif cmd == 'piece':
            if shape:
                b.setFilledFields(shape.field)
            shape = get_shape(b, input().upper())
            shape.setboard(b)
            shape.draw_figure_on_board()
            continue
        elif cmd == 'break':
            b.disappear(shape.field)
            shape = None
            continue
        shape.down()
        shape.draw_figure_on_board()
        if min(shape.state) < 10:
            print('Game Over!')
            break


if __name__ == '__main__':
    main()
