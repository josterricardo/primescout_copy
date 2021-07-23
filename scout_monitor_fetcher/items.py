# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScoutMonitorFetcherItem(scrapy.Item):
    product_name = scrapy.Field()
    product_id = scrapy.Field()
    product_status = scrapy.Field()
    product_prices = scrapy.Field()
    product_details = scrapy.Field()
    product_images = scrapy.Field()
    product_reviews = scrapy.Field()



