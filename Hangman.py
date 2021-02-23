import random

words = ['python', 'java', 'kotlin', 'javascript']

index = random.randint(0, 3)
print('H A N G M A N\n')
while True:
    action = input('Type "play" to play the game, "exit" to quit: ')
    if action == 'exit':
        break
    elif action != 'play':
        continue
    else:        
        word = words[index]
        wordset = set(word)
        player = []
        field = list('-' * len(word))
        print('-' * len(word))
        lives = 8
        while (lives > 0):
            l = input('Input a letter: ')
            if (len(l) != 1):
                print('You should input a single letter')
                if lives >= 1:
                    print('')
                    print(''.join(field))
                continue
            if (l not in 'abcdefghijklmnopqrstuvwxyz'):
                print('Please enter a lowercase English letter') 
                if lives >= 1:
                    print('')
                    print(''.join(field))
                continue
                    
            if (l not in player):
                player.append(l)
            else:
                print("You've already guessed this letter")
                if lives >= 1:
                    print('')
                    print(''.join(field))
                continue
                
            if (l in wordset): 
                for a in range(0, len(word)):
                    if l == word[a]:
                        field[a] = l
            else:
                print("That letter doesn't appear in the word")
                lives -= 1
                
            if lives >= 1:
                print('')
                print(''.join(field))

            if '-' not in ''.join(field):
                break

        if '-' in ''.join(field):
            print('You lost!')
        else:
            print(f'You guessed the word {word}!\nYou survived!')
