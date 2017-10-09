# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EasycrawlItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

    author_born_date = scrapy.Field()
    author_born_location = scrapy.Field()
    author_description = scrapy.Field()
    author_full_url = scrapy.Field()


