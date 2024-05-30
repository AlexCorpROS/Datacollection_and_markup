# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

def category_process(value):
    return value[0].replace('\']','')


class UnsplashItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(outout_processor=TakeFirst())
    url = scrapy.Field(outout_processor=TakeFirst())
    photo = scrapy.Field(outout_processor=TakeFirst())
    category = scrapy.Field(input_processor=Compose(category_process))

# class UnsplashItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     url = scrapy.Field()
#     photo = scrapy.Field()
#     category = scrapy.Field()