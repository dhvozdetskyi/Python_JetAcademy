import requests
import json
from bs4 import BeautifulSoup
import string
import os


def checkQuote(rekw):
    if rekw.status_code != 200:
        print('Invalid quote resource!')
    else:
        try:
            print(rekw.json()["content"])
        except KeyError:
            print('Invalid quote resource!')


def checkMovie(rekw):
    if rekw.status_code != 200:
        print('Invalid movie page!')
    else:
        movies = BeautifulSoup(rekw.content, 'html.parser')
        try:
            movie = dict(json.loads("".join(movies.find("script", {"type":"application/ld+json"}).contents)))
            if 'name' in movie.keys() and 'description' in movie.keys() and movie['@type'] != 'Person':
                res = {'title': movie['name'], 'description': movie['description']}
                print(res)
            else:
                print('Invalid movie page!')
        except AttributeError:
            print('Invalid movie page!')


def saveToFile(r):
    if r.status_code == 200:
        with open('source.html', 'wb') as f:
            f.write(r.content)
        print('Content saved.')
    else:
        print('The URL returned', r.status_code)


def remove_punctuation(value):
    value = value.strip()
    for c in value:
        # If char is not punctuation, add it to the result.
        if c in string.punctuation:
            value = value.replace(c, '')
    return value.translate(value.maketrans(" ", "_"))


def write_file(dir, name, content):
    with open(dir + name + '.txt', 'wb') as file:
        file.write(content)


def parsePage(r, theme, dir):
    global counter
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all('article', {'class': 'u-full-height c-card c-card--flush'})
    founded = []
    for article in articles:
        news = article.find('span', class_='c-meta__type')
        if news.text == theme:
            find_link = article.find('a', {'data-track-action': 'view article'})
            tail = find_link.get('href')
            url = 'https://www.nature.com' + tail
            r_sub = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup_2 = BeautifulSoup(r_sub.content, 'html.parser')
            title = soup_2.find('h1', {'class': 'article-item__title'})
            b_list = soup_2.find('div', class_='article__body')
            if b_list:
                body = b_list.text.strip()
            else:
                b_list = soup_2.find('div', {'class': 'article-item__body'})
                body = b_list.text.strip()

            body_byte = body.encode('utf-8')

            title = remove_punctuation(title.text)
            write_file(dir, title, body_byte)
            founded.append(title + '.txt')
    counter += len(founded)

# r = requests.get(input('Input the URL:\n'), headers={'Accept-Language': 'en-US,en;q=0.5'})
# Stage 1
# checkQuote(r)
# Stage 2
# checkMovie(r)
# Stage 3
# saveToFile(r)
# Stage 4
# parsePage(requests.get('https://www.nature.com/nature/articles', headers={'Accept-Language': 'en-US,en;q=0.5'}), 'News", '')
# Stage 5
pages = int(input())
theme = input()
counter = 0

for i in range(1, pages + 1):
    os.makedirs('Page_' + str(i), exist_ok=True)
    parsePage(requests.get('https://www.nature.com/nature/articles?page=' + str(i), headers={'Accept-Language': 'en-US,en;q=0.5'}), theme, 'Page_' + str(i) + '/')
print('Saved all articles:', counter)


