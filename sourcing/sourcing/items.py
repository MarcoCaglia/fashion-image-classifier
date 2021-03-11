# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZalandoItem(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    brand = scrapy.Field()
    colour = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    pass
