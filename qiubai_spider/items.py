# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ContentItem(scrapy.Item):
	user_name = scrapy.Field()
	user_gender = scrapy.Field()
	user_age = scrapy.Field()
	user_content = scrapy.Field()

class ImgItem(scrapy.Item):
	img_url = scrapy.Field()
	img_path = scrapy.Field()
	img_content = scrapy.Field()