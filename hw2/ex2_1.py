import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
from pprint import pprint

ua = UserAgent()
url = 'https://books.toscrape.com/'
headers = {'User-Agent': ua.random}
params = {'page' : 1}

session = requests.session()

all_books = []

while True:
    response = session.get(url + f"catalogue/page-{params['page']}.html", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('li', {'class': 'col-xs-6'})

    if not posts:
        break

    for post in posts:
        book_info = {}

        book_info['Название'] = post.find('h3').find('a').get('title')
        book_info['Ссылка'] = url + post.find('a').get('href')
        # Из задания не понятно в каком формате хранить данные о цене.
        # book_info['Цена'] = {float(post.find("p", class_="price_color").text.strip().replace("Â\u00a3", "")):'\u00a3'}
        book_info['Цена'] = float(post.find("p", class_="price_color").text.strip().replace("Â\u00a3", ""))
        book_info['Доступно к покупке'] = post.find("p", class_="instock availability").text.strip()

        all_books.append(book_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

with open('list_of_books2.json', 'w') as f:
    json.dump(all_books, f)

pprint(all_books)

'''
Гугл коллаб не может подключиться к среде выполнения, а вывод дает 1000 элементов, потому в комментарии есть пример вывода только нескольких элементов

Мы получили следующий вывод

{'Доступно к покупке': 'In stock',
  'Название': "Alice in Wonderland (Alice's Adventures in Wonderland #1)",
  'Ссылка': 'https://books.toscrape.com/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html',
  'Цена': {55.53: '£'}},
 {'Доступно к покупке': 'In stock',
  'Название': 'Ajin: Demi-Human, Volume 1 (Ajin: Demi-Human #1)',
  'Ссылка': 'https://books.toscrape.com/ajin-demi-human-volume-1-ajin-demi-human-1_4/index.html',
  'Цена': {57.06: '£'}},
 {'Доступно к покупке': 'In stock',
  'Название': "A Spy's Devotion (The Regency Spies of London #1)",
  'Ссылка': 'https://books.toscrape.com/a-spys-devotion-the-regency-spies-of-london-1_3/index.html',
  'Цена': {16.97: '£'}},
 {'Доступно к покупке': 'In stock',
  'Название': "1st to Die (Women's Murder Club #1)",
  'Ссылка': 'https://books.toscrape.com/1st-to-die-womens-murder-club-1_2/index.html',
  'Цена': {53.98: '£'}},
 {'Доступно к покупке': 'In stock',
  'Название': '1,000 Places to See Before You Die',
  'Ссылка': 'https://books.toscrape.com/1000-places-to-see-before-you-die_1/index.html',
  'Цена': {26.08: '£'}}]
'''