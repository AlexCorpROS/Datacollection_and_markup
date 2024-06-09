import scrapy
from scrapy.http import HtmlResponse
from items import OtzovikItem

class OtzovSpider(scrapy.Spider):
    name = "otzov"
    allowed_domains = ["otzovik.com"]
    start_urls = ["https://otzovik.com/reviews/tv-kanal_netflix/"]
    # start_urls = ["https://otzovik.com/reviews/amediateka_ru-onlayn_kinoteatr/"]

    def parse(self, response: HtmlResponse):

        links = response.xpath("//div[@class='item status4 mshow0']")

        for link in links:
            username = link.xpath(".//span[@itemprop='name']/text()").get()
            rating = int(link.xpath(".//div[@class='rating-score tooltip-right']/span/text()").get())
            review_title = link.xpath(".//a[@class='review-title']/text()").get()
            review_teaser = link.xpath(".//div[@class='review-teaser']/text()").get()
            review_plus = link.xpath(".//div[@class='review-plus']/text()").get()
            review_minus = link.xpath(".//div[@class='review-minus']/text()").get()
            comment = review_title + ' ' + review_teaser + ' ' + review_plus + ' ' + review_minus
            yield OtzovikItem(username=username, rating=rating, comment=comment)

            next_page = response.xpath("//a[@class='next tooltip-top button2023']/@href").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
