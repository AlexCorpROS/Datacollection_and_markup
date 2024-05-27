# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pandas as pd


base_dict = []
class CoffeeparserPipeline:
    base_dict = []
    def process_item(self, item, spider):
        base_dict.append(item)
        df = pd.DataFrame.from_dict(base_dict)
        df.to_csv(r'./data/coffee.csv', index=False)
        return item
