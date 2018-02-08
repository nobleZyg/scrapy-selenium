# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    people = scrapy.Field()
    price = scrapy.Field()
    ctime = scrapy.Field()

