# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeatherInfoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    collection = Field()
    date = Field()
    h_temp = Field()
    l_temp = Field()
    info = Field()
    w_dir = Field()
    w_level = Field()
    
