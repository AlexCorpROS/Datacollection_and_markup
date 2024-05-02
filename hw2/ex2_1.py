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

        book_info['Название'] = post.find('h3').text
        book_info['Ссылка'] = url + post.find('a').get('href')
        # Из задания не понятно в каком формате хранить данные о цене.
        book_info['Цена'] = {float(post.find("p", class_="price_color").text.strip().replace("Â\u00a3", "")):'\u00a3'}
        book_info['Доступно к покупке'] = post.find("p", class_="instock availability").text.strip()

        all_books.append(book_info)
    print(f"Обработана {params['page']} страница")
    params['page'] += 1

with open('list_of_books.json', 'w') as f:
    json.dump(all_books, f)

pprint(all_books)