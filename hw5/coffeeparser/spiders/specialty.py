import scrapy
from scrapy.http import HtmlResponse
from items import CoffeeparserItem

class SpecialtySpider(scrapy.Spider):
    name = "specialty"
    allowed_domains = ["specialty.ru"]
    start_urls = ["https://specialty.ru/coffee/"]

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@class='pagination__item pagination__item--next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath("//div[@class='coffee-card__info coffee-card__info_common']/a/@href").getall()
        for link in links:
           yield response.follow(link, callback=self.item_parse)


    def item_parse(self, response:HtmlResponse):
        name = response.xpath("//h1[@class='product-page-info__title glitch-text glitch-text--product-page']/text()").get()
        item_url = response.url
        yield CoffeeparserItem(name=name, url=item_url)