# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import json
import scrapy

class QiubaiSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ImgPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		if item['img_url']:
			img_url = 'http:' + str(item['img_url'])
			yield scrapy.Request(img_url)

	def item_completed(self, results, item, info):
		if results:
			img_path = results[0][1]['path']
			if img_path:
				item['img_path'] = img_path
		return item

class ContentPipeline(object):
	def __init__(self):
		self.fp = open('qiubaiduanzi.json','w+')

	def open_spider(self, spider):
		pass

	def close_spider(self, spider):
		self.fp.close 

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii = False) + '\n'
		self.fp.write(line)	
