def fill_matrix(rows):
    return [input().split() for _ in range(int(rows))]


def init_empty_matrix(rows, cols):
    res = []
    for row in range(rows):
        res.append([])
        for col_ in range(cols):
            res[row].append([])
    return res


def print_matrix(m, rows, cols):
    print('\nThe result is:')
    for row in range(rows):
        for col in range(cols):
            print(m[row][col], end='\t')
        print()
    print()


def bad_entry():
    print('The operation cannot be performed\n')


def matrix_addition(m1_, m2_, rows, cols):
    res = init_empty_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            res[row][col] = float(m1_[row][col]) + float(m2_[row][col])
    return res


def matrix_multiple_by_scalar(m, rows, cols, scalar_):
    res = init_empty_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            res[row][col] = float(m[row][col]) * scalar_
    return res


def matrix_multiple(m1_, m2_, rows, c, cols):
    res = init_empty_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            cell = 0
            for i in range(c):
                cell += float(m1_[row][i]) * float(m2_[i][col])
            res[row][col] = cell
    return res


def matrix_transposition_by_main_diagonal(m, rows, cols):
    res = init_empty_matrix(rows, cols)
    for col in range(cols):
        for row in range(rows):
            res[col][row] = m[row][col]
    return res


def matrix_transposition_by_side_diagonal(m, rows, cols):
    res = init_empty_matrix(rows, cols)
    for col in range(cols - 1, -1, -1):
        for row in range(rows - 1, -1, -1):
            res[cols - 1 - col][rows - 1 - row] = m[row][col]
    return res


def matrix_transposition_by_vert_line(m, rows, cols):
    res = init_empty_matrix(rows, cols)
    for col in range(cols):
        for row in range(rows):
            res[row][cols - 1 - col] = m[row][col]
    return res


def matrix_transposition_by_horz_line(m, rows, cols):
    res = init_empty_matrix(rows, cols)
    for col in range(cols):
        for row in range(rows):
            res[rows - 1 - row][col] = m[row][col]
    return res


def fill_singleton_matrix(isSquare=True):
    r_c_input = input('Enter matrix size: ').strip()
    if r_c_input.count(' ') == 1:
        r, c = map(int, r_c_input.split())
        if isSquare and r != c:
            bad_entry()
            return None, 0, 0
    else:
        bad_entry()
        return None, 0, 0
    print('Enter matrix: ')
    return fill_matrix(r), r, c


def matrix_transposition(t_choice):
    m, r, c = fill_singleton_matrix()
    if m is not None:
        if t_choice in (1, 2, 3, 4):
            if t_choice == 1:
                res = matrix_transposition_by_main_diagonal(m, r, c)
            elif t_choice == 2:
                res = matrix_transposition_by_side_diagonal(m, r, c)
            elif t_choice == 3:
                res = matrix_transposition_by_vert_line(m, r, c)
            else:
                res = matrix_transposition_by_horz_line(m, r, c)
            print_matrix(res, r, c)
        else:
            bad_entry()


def get_minor(m, row, col):
    res = init_empty_matrix(len(m), len(m))
    for r in range(len(m)):
        for c in range(len(m)):
            res[r][c] = m[r][c]
    for r in range(len(res)):
        del res[r][col]
    del res[row]
    return res


def determinant(m):
    if len(m) == 2:
        return float(m[0][0]) * float(m[1][1]) - float(m[1][0]) * float(m[0][1])
    elif len(m) == 1:
        return float(m[0][0])
    else:
        d = 0.0
        for col in range(len(m[0])):
            d += (-1) ** col * float(m[0][col]) * determinant(get_minor(m, 0, col))
        return float(d)


def matrix_determinant():
    m, r, c = fill_singleton_matrix()
    if m is not None:
        print('\nThe result is:')
        print(determinant(m))


def matrix_inversion():
    m, r, c = fill_singleton_matrix()
    if m is not None:
        det = determinant(m)
        if det == 0.0:
            print("This matrix doesn't have an inverse.")
        else:
            inv = init_empty_matrix(r, c)
            for row in range(r):
                for col in range(c):
                    inv[row][col] = (-1) ** ((row + 1) + (col + 1)) * determinant(get_minor(m, row, col))

            trans = matrix_transposition_by_main_diagonal(inv, r, c)
            final = matrix_multiple_by_scalar(trans, r, c, 1 / det)
            print_matrix(final, r, c)
    else:
        return 0


def menu_transposition():
    print('''1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line\n''')
    return int(input('Your choice: '))


def menu():
    print('''1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit\n''')
    return int(input('Your choice: '))


choice = menu()
while choice != 0:
    if choice in (4, 5, 6):
        if choice == 4:
            matrix_transposition(menu_transposition())
        elif choice == 5:
            matrix_determinant()
        else:
            matrix_inversion()
    elif choice in (1, 3):
        m1, m2, r1, c1, r2, c2 = None, None, 0, 0, 0, 0
        r_c1_input = input('Enter size of first matrix: ').strip()
        if r_c1_input.count(' ') == 1:
            r1, c1 = map(int, r_c1_input.split())
            print('Enter first matrix: ')
            m1 = fill_matrix(r1)
            r_c2_input = input('Enter size of second matrix: ').strip()
            if r_c2_input.count(' ') == 1:
                r2, c2 = map(int, r_c2_input.split())
                print('Enter second matrix: ')
                m2 = fill_matrix(r2)
            else:
                bad_entry()
        else:
            bad_entry()
        if m1 is not None and m2 is not None:
            if choice == 1:
                if r1 == r2 and c1 == c2:
                    res = matrix_addition(m1, m2, r1, c1)
                    print_matrix(res, r1, c1)
                else:
                    bad_entry()
            else:
                if c1 == r2:
                    res = matrix_multiple(m1, m2, r1, c1, c2)
                    print_matrix(res, r1, c2)
                else:
                    bad_entry()
    elif choice == 2:
        m, r, c = fill_singleton_matrix(False)
        scalar = float(input('Enter constant: '))
        res = matrix_multiple_by_scalar(m, r, c, scalar)
        print_matrix(res, r, c)
    else:
        bad_entry()
    choice = menu()
