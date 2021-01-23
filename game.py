import random

name = input('Enter your name: ')
print('Hello,', name)

rating = open('rating.txt', 'r')
score = 0
for line in rating:
    n, s = line.split()
    if n == name:
        score = int(s)
        break 
rating.close()

options = input()
if options == '':
    options = ['rock', 'scissors', 'paper']
else:
    options = options.split(',')

print("Okay, let's start")

while True:
    user_choice = input()
    if user_choice == '!exit':
        print('Bye!')
        break
    elif user_choice == '!rating':
        print('Your rating:', score)    
    elif user_choice in options:    
        comp_choice = random.choice(options)
        if user_choice == comp_choice:
            print('There is a draw ({})'.format(comp_choice))
            score += 50
        else:
            if options == ['rock', 'scissors', 'paper']:
                if (user_choice == 'rock' and comp_choice == 'scissors') or (user_choice == 'scissors' and comp_choice == 'paper') or (user_choice == 'paper' and comp_choice == 'rock'):
                    print('Well done. The computer chose {} and failed'.format(comp_choice))   
                    score += 100
                else:
                    print('Sorry, but the computer chose {}'.format(comp_choice))
            else:
                u_c_i = options.index(user_choice) 
                opt = options[u_c_i + 1:]
                opt.extend(options[:u_c_i])
                c_c_i = opt.index(comp_choice)
                if c_c_i >= len(opt) // 2:            
                    print('Well done. The computer chose {} and failed'.format(comp_choice))   
                    score += 100
                else:
                    print('Sorry, but the computer chose {}'.format(comp_choice))
    else:
        print('Invalid input')           
