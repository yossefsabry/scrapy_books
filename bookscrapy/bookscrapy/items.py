# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# for serialize the data for the price and price and tax
# def serialize(value):
#     return f"{str(value)}"

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    product_type = scrapy.Field()
    price = scrapy.Field()
    price_and_tax = scrapy.Field()
    availability = scrapy.Field()
    rating_star = scrapy.Field()
    description = scrapy.Field()
    categroy = scrapy.Field()