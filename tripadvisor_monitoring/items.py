# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tripadvisor_monitoringItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #Hotel Info
    review_code = scrapy.Field()
    review_text = scrapy.Field()
    response_text = scrapy.Field()
    rating = scrapy.Field()

