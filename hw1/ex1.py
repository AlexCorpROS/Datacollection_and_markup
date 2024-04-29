import json
import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
def user_request(save = False):
    url = "https://api.foursquare.com/v3/places/search"

    point_interest = input("Введите название интересующей Вас категории: ")

    params = {
        'limit': 10,
        'query': point_interest,
        'fields': 'name,location,rating'
    }

    headers = {
        "User-Agent": os.getenv('USER_AGENT'),
        "Accept": "application/json",
        "Authorization": os.getenv('API_AUTH'),
    }

    response = requests.request("GET", url, params=params, headers=headers)

    if response.status_code == 200:
        print("Успешный запрос API по URL: ", response.url)
    else:
        print("Запрос API отклонен с кодом состояния:", response.status_code)

    data = response.json()

    obj_interest = []

    for place in data['results']:
        place_name = place.get('name')
        place_address = place.get('location')['formatted_address']
        place_rating = place.get('rating') if 'rating' in place else "Рейтинг не определялся"
        obj_interest.append({'name': place_name, 'address': place_address, 'rating': place_rating})

    for obj in obj_interest:
            print(f"Название: {obj['name']}")
            print(f"Адрес: {obj['address']}")
            print(f"Рейтинг: {obj['rating']}")
            print()

    # Если нам нужно сохранить данные запроса, то в функции передаем какой либо аргумент.
    if save != False:
        with open('user_data.json','w') as f:
            json.dump(data,f)


user_request()


'''
На запрос "парк" мы получаем слeдующий вывод

"C:\Work\GB\Вторая четверть\Datacollection_and_markup\venv\Scripts\python.exe" "C:\Work\GB\Вторая четверть\Datacollection_and_markup\hw1\ex1.py" 
Введите название интересующей Вас категории: парк
Успешный запрос API по URL:  https://api.foursquare.com/v3/places/search?limit=10&query=%D0%BF%D0%B0%D1%80%D0%BA&fields=name%2Clocation%2Crating
Название: Парк Островского
Адрес: 344000, Ростов-на-Дону
Рейтинг: 8.1

Название: Парк им. Вити Черевичкина
Адрес: Ростов-на-Дону
Рейтинг: 6.7

Название: Парк культуры и отдыха имени Октября
Адрес: Ул. 56-й Армии, 344000, Ростов-на-Дону
Рейтинг: 8.4

Название: новый левобережный парк
Адрес: 344000, Ростов-на-Дону
Рейтинг: 7.9

Название: Парк имени города Плевен
Адрес: просп. Стачки, Ростов-на-Дону
Рейтинг: 8.4

Название: Парк им. Максима Горького
Адрес: ул. Пушкинская, Ростов-на-Дону
Рейтинг: 7.5

Название: парк им. К. Чуковского
Адрес: пер. Ставропольский/ул. Цезаря Куникова, Ростов-на-Дону
Рейтинг: 7.5

Название: Покровский сквер
Адрес: просп. Кировский, Ростов-на-Дону
Рейтинг: 8.6

Название: Улица Пушкинская
Адрес: Кировский проспект, Ростов-на-Дону
Рейтинг: 8.1

Название: Сквер Восточный
Адрес: Азов
Рейтинг: 7.5

'''