'''
В данной реализации категорию изображений будет задавать сам пользователь. Этот же параметр будет использоваться вместо хештегов
и определять место хранения загруженных изображений.
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