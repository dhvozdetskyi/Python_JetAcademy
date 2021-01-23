import random
import sqlite3


class Card:
    def __init__(self, card_number, card_pin, card_balance):
        self.number = card_number
        self.pin = card_pin
        self.balance = card_balance


conn = sqlite3.connect('./card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()


def menu1():
    print('''1. Create an account
2. Log into account
0. Exit
    ''')
    return int(input())


def menu2():
    print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
    ''')


def check_sum(number_):
    i, sum_ = 1, 0
    for a in number_:
        sum_ += (int(a) * 2 - 9 if int(a) * 2 > 9 else int(a) * 2) if i % 2 == 1 else int(a)
        i += 1
    return '0' if sum_ % 10 == 0 else str(10 - sum_ % 10)


def generate_card_number():
    num = str(random.randrange(0, 999999999))
    if len(num) < 9:
        num = '0' * (9 - len(num)) + num
    number_ = '400000' + num
    return number_ + check_sum(number_)


def check_card_number(card_number):
    return card_number == card_number[:-1] + check_sum(card_number[:-1])


def add_income(account):
    cur.execute('UPDATE card SET balance = balance + ? where number = ?;', (int(input('Enter income:')), account[0]))
    conn.commit()
    cur.execute('SELECT number, pin, balance FROM card WHERE number = ? AND pin = ?;', (account[0], account[1]))
    return cur.fetchone()


def close_account(card_number):
    cur.execute('DELETE FROM card where number = ?;', (card_number,))
    conn.commit()


def do_transfer(account):
    print('Transfer\nEnter card number:')
    cn = input()
    if not check_card_number(cn):
        print('\nProbably you made a mistake in the card number. Please try again!\n')
    else:
        cur.execute('SELECT number FROM card WHERE number = ?;', (cn,))
        target = cur.fetchone()
        if target is None:
            print('\nSuch a card does not exist.\n')
        elif target[0] == account[0]:
            print("You can't transfer money to the same account!")
        else:
            transfer = int(input('Enter how much money you want to transfer:'))
            cur.execute('SELECT balance FROM card WHERE number = ? AND pin = ?;', (account[0], account[1]))
            if cur.fetchone()[0] < transfer:
                print('Not enough money!')
            else:
                cur.execute('UPDATE card SET balance = balance - ? where number = ?;', (transfer, account[0]))
                conn.commit()
                cur.execute('UPDATE card SET balance = balance + ? where number = ?;', (transfer, cn))
                conn.commit()
                cur.execute('SELECT number, pin, balance FROM card WHERE number = ? AND pin = ?;', (account[0], account[1]))
                print('Success!')
                return cur.fetchone()
    return account


select1 = menu1()
while select1 != 0:
    if select1 == 1:
        print('\nYour card has been created\n')
        pin = str(random.randrange(1, 9999))
        if len(pin) < 4:
            pin = '0' * (4 - len(pin)) + pin
        while True:
            number = generate_card_number()
            cur.execute('SELECT id FROM card WHERE number = ?', (number,))
            row = cur.fetchone()
            if row is not None:
                print('\nSuch number already exists. Try again!\n')
                select1 = menu1()
                continue
            else:
                cur.execute('INSERT INTO card (number, pin) VALUES (?, ?);', (number, pin))
                conn.commit()
                print('Your card number:\n{}'.format(number))
                print('Your card PIN:\n{}\n'.format(pin))
                break
        select1 = menu1()
    elif select1 == 2:
        c_number = input('\nEnter your card number:\n')
        c_pin = input('Enter your PIN:\n')
        cur.execute('SELECT number, pin, balance FROM card WHERE number = ? AND pin = ?;', (c_number, c_pin))
        row = cur.fetchone()
        if row is not None:
            print('\nYou have successfully logged in!\n')
            menu2()
            while True:
                select2 = int(input())
                if select2 == 1:
                    print('\nBalance: {}\n'.format(row[2]))
                    menu2()
                elif select2 == 2:
                    row = add_income(row)
                    print('\nIncome was added!\n')
                    menu2()
                elif select2 == 3:
                    row = do_transfer(row)
                    menu2()
                elif select2 == 4:
                    close_account(row[0])
                    print('\nThe account has been closed!\n')
                    select1 = menu1()
                    break
                elif select2 == 5:
                    print('\nYou have successfully logged out!\n')
                    select1 = menu1()
                    break
                elif select2 == 0:
                    select1 = 0
                    break
        else:
            print('\nWrong card number or PIN!\n')
            select1 = menu1()
print('Bye!')
