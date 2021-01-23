import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

dir_for_files = sys.argv[1]
os.makedirs(dir_for_files, exist_ok=True)

stack, prev, tags = [], '', ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
init()
addressURL = input()
while True:
    if addressURL == 'exit':
        break
    elif addressURL == 'back':
        if stack:
            file = open('/'.join((dir_for_files, stack.pop())), 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()
            for line in lines:
                if line.strip() != '':
                    print(line)
    elif addressURL.find('.') == -1:
        print('Error: Incorrect URL')
    else:
        if not addressURL.startswith('https://'):
            addressURL = 'https://' + addressURL
        r = requests.get(addressURL)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            filename = addressURL[addressURL.index('//') + 2:] if '.' not in addressURL else addressURL[addressURL.index('//') + 2:addressURL.rindex('.')]
            soup = BeautifulSoup(r.content, 'html.parser')
            lst = soup.find_all(tags)
            file = open('/'.join((dir_for_files, filename)), 'w', encoding='utf-8')
            try:
                for tag in lst:
                    if str(tag)[:2] == '<a':
                        prefix = Fore.BLUE
                    else:
                        prefix = Style.RESET_ALL
                    print(prefix + tag.text)
                    file.write(prefix + tag.text + '\n')
            finally:
                file.close()
            prev = filename
        else:
            print('Error: Incorrect URL')
    addressURL = input()
    if addressURL != 'back' and prev:
        stack.append(prev)
        prev = ''
