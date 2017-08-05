# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quote = scrapy.Field()
    reviewBody = scrapy.Field()
    stars = scrapy.Field()
    reviewDate = scrapy.Field()
    _id = scrapy.Field()
