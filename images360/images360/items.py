# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class Images360Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'images'   # collection代表MongoDB存储的Collection名称;table代表MySQL存储的表名称
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()
