# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZlItem(scrapy.Item):
    title = scrapy.Field()
    openNo = scrapy.Field()
    openDate= scrapy.Field()
    applyNo = scrapy.Field()
    applyDate= scrapy.Field()
    applyPeople = scrapy.Field()
    inventor = scrapy.Field()
    address = scrapy.Field()
    classifyNo = scrapy.Field()
    summery = scrapy.Field()
    qrcodeurls = scrapy.Field()
    thumb = scrapy.Field()

class DownurlItem(scrapy.Item):
    downurl = scrapy.Field()
    applyNo = scrapy.Field()