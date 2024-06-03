import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
num_requests = 100 # количество элементов в запросе для ситуаций с неточным поиском или автозаполнением страницы данными
file = 'yula_data.json'

options = Options()
options.add_argument('start-maximized')
options.add_argument(f'user_agent={user_agent}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)


# driver.get('https://www.twitch.tv/directory')
driver.get('https://youla.ru/rostov-na-donu')
input = driver.find_element(By.XPATH, '//input')
input.send_keys('стиральная машина')
input.send_keys(Keys.ENTER)
time.sleep(5)


try:
    while True:
        expectant = WebDriverWait(driver, 20)
        cards = expectant.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-test-component='ProductOrAdCard']")))
        # cards = driver.find_elements(By.XPATH, "//div[@class='Layout-sc-1xcs6mc-0 iAEkom']")
        print(len(cards))
        count = len(cards)
        # Прокрутка на определенное количество пикселей
        # driver.execute_script("window.scrollBy(0, 1000)")
        # Прокрутка до низа страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)

        '''
        Выбранный для изучения сайт не работает без JavaScript, а потому эффективно извлечь из него данные изучаемыми инструментами
        проблематично.Потому мы будем извлекать все доступные текстовые данные из динамических карточек объявлений.
        Пустые будем пропускать.
        '''
        cards = driver.find_elements(By.XPATH, "//div[@data-test-component='ProductOrAdCard']")
        data = []
        for card in cards:
            name = card.text
            if name != "":
                data_card = {
                    'Объявление': name,
                }
                data.append(data_card)
                with open(file, 'w', encoding='utf-8') as js:
                    json.dump(data, js, ensure_ascii=False)

        # Описываем условия выход из цикла.
        if len(cards) == count or len(cards)> num_requests:
            break

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()


    