# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from easycrawl.misc.store import quotesbotDB


class EasycrawlPipeline(object):
    def process_item(self, item, spider):
        if spider.name != "toscrape-css":  return item
        if item.get("text", None) is None: return item

        spec = { "text": item["text"] }
        quotesbotDB.quotebot.update(spec, {'$set': dict(item)}, upsert=True)

        return None
