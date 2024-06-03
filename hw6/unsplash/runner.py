'''
В данной реализации категорию изображений будет задавать сам пользователь. Этот же параметр будет использоваться вместо хештегов
и определять место хранения загруженных изображений.
Для экономии памяти код на гитхабе не будет содержать собранных данных и загруженных изображений.
В качестве примера работы кода на лдокальном устройсте будет запущен код с параметром 'cars'.
Результат работы кода в виде csv файла будет прикреплен в форме сдачи задания.
'''

from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.unsp import UnspSpider

if __name__ == '__main__':
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    process = CrawlerProcess(get_project_settings())
    category = str(input('Введите название категории изображений:'))
    process.crawl(UnspSpider, query=category)
    process.start()