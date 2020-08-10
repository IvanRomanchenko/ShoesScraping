# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from pymongo import MongoClient


class JsonWriterPipeline:
    """ Creates a JSON-file with written in it items """
    
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


class FirstMongoDbWriterPipeLine:
    """ First addition of scraped items in DB"""
    
    def open_spider(self, spider):
        client = MongoClient("mongodb+srv://Viewer:YPNuBSC0EjLJWvoc@cluster0.ep7vi.mongodb.net/selfy_db?retryWrites=true&w=majority")
        self.collection = client.selfy_db.shoes
        
    def process_item(self, item, spider):
        self.collection.insert_one(ItemAdapter(item).asdict())
        return item     


class UpdatingMongoDbWriterPipeLine:
    """ Supplements the DB """
    
    def open_spider(self, spider):
        client = MongoClient("mongodb+srv://Viewer:YPNuBSC0EjLJWvoc@cluster0.ep7vi.mongodb.net/selfy_db?retryWrites=true&w=majority")
        self.collection = client.selfy_db.shoes
        self.documents = []
        for i in self.collection.find({}):
            del i['_id']
            self.documents.append(i)

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        if item_dict not in self.documents:
            self.collection.insert_one(item_dict)
        return item


'''
# Another method for supplements a database
# More graceful but slower (in practice)
class UpdatingMongoDbWriterPipeLine:
    """ Supplements the DB """
    
    def open_spider(self, spider):
        client = MongoClient("mongodb+srv://Viewer:YPNuBSC0EjLJWvoc@cluster0.ep7vi.mongodb.net/selfy_db?retryWrites=true&w=majority")
        self.collection = client.selfy_db.shoes

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        self.collection.update_one({'name': item_dict['name']}, {'$set': item_dict}, upsert=True)
        return item
'''
