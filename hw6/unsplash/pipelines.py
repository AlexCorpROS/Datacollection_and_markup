# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import hashlib
from scrapy.pipelines.images import ImagesPipeline
import pandas as pd


# class UnsplashPipeline:
#     def process_item(self, item, spider):
#         return item
base_dict = []

class UnsplashPipeline:
    base_dict = []
    def process_item(self, item, spider):
        base_dict.append(item)
        df = pd.DataFrame.from_dict(base_dict)
        df.to_csv(f"./data/{item['category'][0]}.csv", index=False)
        return item

class PhotoPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        return f"{item['category'][0]}/{item['name']}-{image_guid}.jpg"

    def get_media_requests(self, item, info):
        if item['photo']:
            for url in item['photo']:
                try:
                    yield scrapy.Request(url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print()
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item