""" Model for scrapped Item """

import re
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_quotes(text):
    """
    Removes Quotes, backslash and unicode characters
    """
    return ''.join([i if ord(i) < 128 else ' ' for i in text.strip()])\
        .replace('\\','').replace('"','').replace('\r','').replace('\n','')

def remove_alphabets_from_price(text):
    """ Removes any character other than digit """
    return re.sub(r'\D', '', text.strip())

class ProductItem(Item):
    """ Item class for Each LED instance"""
    name = Field(
        input_processor=MapCompose(remove_quotes),
        output_processor=TakeFirst()
    )
    link = Field(
        output_processor=TakeFirst()
    )
    image_link = Field(
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(remove_alphabets_from_price),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(remove_quotes),
        output_processor=Join()
    )
