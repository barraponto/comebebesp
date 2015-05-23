# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapylib.processors import default_input_processor, default_output_processor


class ComebebespItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    neighborhood = scrapy.Field()
    city = scrapy.Field()
    telephone = scrapy.Field()
    website = scrapy.Field()
    category = scrapy.Field()


class ComebebespItemLoader(ItemLoader):
    default_item_class = ComebebespItem
    default_output_processor = default_output_processor
    default_input_processor = default_input_processor
