import requests
from lxml import html
import csv
import pandas as pd
from fake_useragent import UserAgent ### Для указания агента пользователя
import re
from urllib.parse import urljoin

### Предлагаю для парсинга выбрать таблицу из русской Википедии со статистикой численности населения городов России с населением более 100 тысяч жителей.
### Первые два столбца с рангами городов предлагаю не сохранять, т.к. в них нет необходимости, т.к. рейтинг можно вычислить на основании данных распарсиных из этой таблицы.

url_base = "https://ru.wikipedia.org"
url = "https://ru.wikipedia.org/wiki/Список_городов_России_с_населением_более_100_тысяч_жителей"

ua = UserAgent() #### для указания "браузера"
headers = {
    "User-Agent": ua.firefox, ### генерируем данные браузера Мозила
}

# Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
try:
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        print("Успешный запрос API по URL: ", response.url)
    else:
        print("Запрос API отклонен с кодом состояния:", response.status_code)

except requests.exceptions.RequestException as e:
    print("Ошибка в осущественнии HTML запроса:", e)

# Парсинг HTML-содержимого ответа с помощью библиотеки lxml с обработкой исключительных ситуаций
try:
    tree = html.fromstring(response.content)
    print(tree)
except html.etree.ParserError as e:
    print("Ошибка в парсинге HTML содержимого:", e)

try:
    table_rows = tree.xpath("//table[@class='wikitable sortable']/tbody/tr")
    len(table_rows)

except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)

### получаем заголовки столбцов таблицы
try:
    years = table_rows[0].xpath("//th/span/text()")[2:]
    print(years)

except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)

### Добавляем два столбца в заголовок таблицы - название города и ссылку на другую страницу в Википедии, где описана подробная информациия о городе
years.insert(0, "Город")
years.append("Ссылка на информацию о городе")

### Создаем заготовку для таблицы (пустую таблицу) с названиями столбцов
df = pd.DataFrame(columns = years)
print(years)

### Собственно парсинг таблицы
try:
    for row in table_rows[2:]:
        ### Работа с каждой ячейкой таблицы отдельно
        cells = row.xpath('.//td|.//th')[2:]

        ### Если в ячейке таблицы значения нет, то возвращаем None
        row_data = [cell.text_content().strip() if cell.text_content().strip() else None for cell in cells]

        ### Если в ячейке таблицы прочерк, то замещаем его на None
        row_data = [None if item == '—' else item for item in row_data]

        ### убираем референсные ссылки на источники статистических данных
        row_data = [re.sub("\[[0-9]+\]", '', s) if s is not None else None for s in row_data]

        ### получаем ссылку на информацию о городе
        city_wiki_ref = urljoin(url_base, row.xpath(".//td//a/@href")[0])

        ### Объединяем данные из строки в итоговую таблицу
        temp_df = pd.DataFrame(data=row_data)
        temp_df = temp_df.transpose()
        temp_df.columns = years[:-1]
        temp_df["Ссылка на информацию о городе"] = city_wiki_ref
        df = pd.concat([df, temp_df])
        # print(temp_df)

except IndexError as e:
    print("Ошибка доступа к результату:", e)

except Exception as e:
    print("Произошла непредвиденная ошибка:", e)