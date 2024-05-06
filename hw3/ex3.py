import json
from pymongo import MongoClient

# with open("list_of_books.json", "r", encoding='utf-8') as file:
#     data = json.load(file)
#
# print(data[2])

client = MongoClient('localhost', 27017)
db = client['books']
collection = db['book']

# Данные в нашу базу данных мы загрузили с помощью графической оболочки compass. Проверим сколько у нас элементов.
elements = collection.count_documents({})
print("Количество записей в коллекции book:", elements)

# В базе более 1000 элементов, потому сузим запрос до книг дороже 59.9
price = collection.find({"Цена": {"$gt": 59.9}})
for i in price:
    print("Книги дороже 59.9:", i)

# Так же модем использовать сортировки и настройку запроса
price2 = collection.find({"Цена": {"$gt": 50}}).sort({"Цена": 1}).limit(5)
for i in price2:
    print("Первые пять книг дороже 50, отсортированные по возрастанию цены:", i)

'''
Мы получаем следующий вывод

Количество записей в коллекции book: 1000
Книги дороже 50: {'_id': ObjectId('6638d54e60a6316471eade30'), 'Название': 'Soumission', 'Ссылка': 'https://books.toscrape.com/soumission_998/index.html', 'Цена': 50.1, 'Доступно к покупке': 'In stock'}
Книги дороже 50: {'_id': ObjectId('6638d54e60a6316471eae140'), 'Название': 'Rogue Lawyer (Rogue Lawyer #1)', 'Ссылка': 'https://books.toscrape.com/rogue-lawyer-rogue-lawyer-1_214/index.html', 'Цена': 50.11, 'Доступно к покупке': 'In stock'}
Книги дороже 50: {'_id': ObjectId('6638d54e60a6316471eae0b5'), 'Название': "The Pilgrim's Progress", 'Ссылка': 'https://books.toscrape.com/the-pilgrims-progress_353/index.html', 'Цена': 50.26, 'Доступно к покупке': 'In stock'}
Книги дороже 50: {'_id': ObjectId('6638d54e60a6316471eade5c'), 'Название': 'We Love You, Charlie Freeman', 'Ссылка': 'https://books.toscrape.com/we-love-you-charlie-freeman_954/index.html', 'Цена': 50.27, 'Доступно к покупке': 'In stock'}
Книги дороже 50: {'_id': ObjectId('6638d54e60a6316471eae036'), 'Название': 'Nightstruck: A Novel', 'Ссылка': 'https://books.toscrape.com/nightstruck-a-novel_480/index.html', 'Цена': 50.35, 'Доступно к покупке': 'In stock'}

Весь надор команд можно изучить по ссылке https://www.mongodb.com/docs/manual/reference/command/

К сожалению облачный сервис MongoDB не доступен в нашей стране. Это касается и сервиса ClickHouse.

ClickHouse Cloud is not available in your country
Service creation is not available in your country, which means that you cannot use ClickHouse as a hosted database service.

You can still use your account to gain access to training or to paid support for your self managed ClickHouse.

По этой причине глубокое изучение этих инструментов выглядит малоперспективным и стоит найти аналоги работающие в нашей стране.
'''

