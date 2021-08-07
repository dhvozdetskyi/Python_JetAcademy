import random

stock, domino_snake = [], []


def FillStock():
    for i in range(7):
        for j in range(7):
            if not [j, i] in stock:
                stock.append([i, j])

def CheckPieceIsPlayablePlayer(piece, side):
    if (domino_snake[0][0] in piece) or (domino_snake[-1][1] in piece):
        if domino_snake[0][0] != domino_snake[-1][1]:
            if piece[0] != piece[1]:
                if ((piece[1] == domino_snake[0][0]) and (side == '-')) or ((piece[0] == domino_snake[-1][1]) and (side == '+')):
                    return True, False
                else:
                    return True, True
            else:
                return True, False
        else:
            return True, False
    else:
        return False, None


def CheckPieceIsPlayablePC(piece):
    if (domino_snake[0][0] in piece) or (domino_snake[-1][1] in piece):
        if domino_snake[0][0] != domino_snake[-1][1]:
            if piece[0] != piece[1]:
                if (piece[1] == domino_snake[0][0]):
                    return True, False, 'l'
                elif (piece[0] == domino_snake[-1][1]):
                    return True, False, 'r'
                elif (piece[0] == domino_snake[0][0]):
                    return True, True, 'l'
                elif (piece[1] == domino_snake[-1][1]):
                    return True, True, 'r'
            else:
                return True, False, 'r'
        else:
            return True, False, 'r'
    else:
        return False, None, ''


FillStock()

while not domino_snake:
    random.shuffle(stock)
    player_pieces = random.sample(stock, 7)
    computer_pieces = random.sample([i for i in stock if i not in player_pieces], 7)
    stock_pieces = [i for i in stock if i not in player_pieces and i not in computer_pieces]
    player_double = [piece for piece in player_pieces if piece[0] == piece[1]]
    computer_double = [piece for piece in computer_pieces if piece[0] == piece[1]]
#    if player_double == [] and computer_double == []:
#        continue
#    if not player_double:
#        domino_snake.append(max(max(computer_double)))
#    elif not computer_double:
#        domino_snake.append(max(max(player_double)))
#    else:
#        domino_snake.append(max(max(computer_double), max(player_double)))
    if player_double == []:
        continue
    domino_snake.append(max(player_double))


status = "computer" if domino_snake[0] in player_pieces else "player"
if status == "player":
    for i in computer_pieces:
        if i == domino_snake[0]:
            computer_pieces.remove(i)
            break
else:
    for i in player_pieces:
        if i == domino_snake[0]:
            player_pieces.remove(i)
            break

while True:
    print("=" * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()
    if len(domino_snake) <= 6:
        print(*domino_snake, sep='')
    else:
        print(*domino_snake[0:3], '...', *domino_snake[-3:], sep='')
    print()
    print('Your pieces:')
    n = 1
    for piece in player_pieces:
        print(f'{n}:{piece}')
        n += 1
    print()
    if len(player_pieces) == 0:
        print('Status: The game is over. You won!')
        break
    if len(computer_pieces) == 0:
        print('Status: The game is over. The computer won!')
        break
    print("Status:", "It's your turn to make a move. Enter your command." if status == 'player' else 'Computer is about to make a move. Press Enter to continue...')

    c = input().strip()
    if status == 'player':
        try:
            piece_idx = int(c)
        except:
            print('Invalid input. Please try again.')
            continue

        if not (-len(player_pieces) <= piece_idx <= len(player_pieces)):
            print('Invalid input. Please try again.')
            continue

        if piece_idx == 0:
            if len(stock_pieces) > 0:
                piece_idx = random.randint(-len(stock_pieces), len(stock_pieces))
                if piece_idx == 0:
                    piece_idx = 1
                player_pieces.append(stock_pieces[abs(piece_idx) - 1])
                stock_pieces.pop(abs(piece_idx) - 1)
                status = 'computer'
                continue
            else:
                print("Status: The game is over. It's a draw!")
                break
        playable, do_rotate = CheckPieceIsPlayablePlayer(player_pieces[abs(piece_idx) - 1], '-' if piece_idx < 0 else '+')
        if playable:
            if do_rotate:
                piece = player_pieces[abs(piece_idx) - 1][::-1]
            else:
                piece = player_pieces[abs(piece_idx) - 1]
            if piece_idx >= 1:
                domino_snake.append(piece)
            else:
                domino_snake.insert(0, piece)
            player_pieces.pop(abs(piece_idx) - 1)
            status = 'computer'
        else:
            print('Illegal move. Please try again.')
            continue
    else:
        playable, draw, side, piece = False, False, '', None
        dict_count = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
        for p in computer_pieces:
            dict_count[str(p[0])] += 1
            dict_count[str(p[1])] += 1
        for p in domino_snake:
            dict_count[str(p[0])] += 1
            dict_count[str(p[1])] += 1
        score = {}
        for i in range(len(computer_pieces)):
            score[str(i)] = dict_count[str(computer_pieces[i][0])] + dict_count[str(computer_pieces[i][1])]

        ordered = sorted(score.values(), reverse=True)
        for i in ordered:
            for idx in range(len(computer_pieces)):
                if dict_count[str(computer_pieces[idx][0])] + dict_count[str(computer_pieces[idx][1])] == i:
                    piece = computer_pieces[idx]
                    break
            playable, do_rotate, side = CheckPieceIsPlayablePC(piece)
            if playable:
                break

        if not playable:
            if len(stock_pieces) > 0:
                piece_idx = random.randint(-len(stock_pieces), len(stock_pieces))
                if piece_idx == 0:
                    piece_idx = 1
                computer_pieces.append(stock_pieces[abs(piece_idx) - 1])
                stock_pieces.pop(abs(piece_idx) - 1)
                status = 'player'
                continue
            else:
                print("Status: The game is over. It's a draw!")
                draw = True
                break

        for i in computer_pieces:
            if i == piece:
                computer_pieces.remove(i)
                break

        if do_rotate:
            piece = piece[::-1]

        if side == 'r':
            domino_snake.append(piece)
        else:
            domino_snake.insert(0, piece)

        status = 'player'
