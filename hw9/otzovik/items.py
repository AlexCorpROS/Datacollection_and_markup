# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OtzovikItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    rating = scrapy.Field()
    comment = scrapy.Field()
    # review_title = scrapy.Field()
    # review_teaser = scrapy.Field()
    # review_plus = scrapy.Field()
    # review_minus = scrapy.Field()

