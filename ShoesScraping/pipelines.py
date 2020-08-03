# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pymongo


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.item_list = []

    def close_spider(self, spider):
        num_id = 0
        for i in self.item_list:
            num_id += 1
            i['_id'] = num_id
        json.dump(self.item_list, self.file, ensure_ascii=False, indent=2)
        self.file.close()

    def process_item(self, item, spider):
        self.item_list.append(ItemAdapter(item).asdict())
        return item