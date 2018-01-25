# -*-coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from bs4 import BeautifulSoup as BS
from qiubai_spider.items import ContentItem,ImgItem
import re

class QiubaiSpider(scrapy.Spider):
	name = 'qiubaispider'

	def __init__(self):
		self.first_url = 'https://www.qiushibaike.com/'
		self.url_len = len(self.first_url)
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		self.headers = {'User-Agent': user_agent}

	def start_requests(self):
		return [scrapy.Request(self.first_url, headers = self.headers,callback = self.get_list)]

	def get_list(self, response):
		soup = BS(response.body, 'html.parser')
		user_links = soup.find_all('a', attrs = {'href':re.compile(r'/article/.*')})
		for user_link in user_links:
			try:
				link = user_link['href']
				full_link = self.first_url[0:self.url_len-1] + str(link)	
				yield scrapy.Request(full_link, headers = self.headers,callback = self.get_content)
			except:
				print 'get user content error!'

		next_links = soup.find('ul', class_ = 'pagination').find_all('li')
		for next_link in next_links:
			try:
				next_url = next_link.find('a')['href']	
				if next_url:
					url = self.first_url[0:self.url_len-1] + str(next_url)
					yield scrapy.Request(url, headers = self.headers, callback=self.get_list)
			except:
				print "find next page error!"

	def get_content(self, response):
		content_item = ContentItem()
		soup = BS(response.body, 'html.parser')
		user_content = soup.find('div', class_= 'article')
		content_item['user_name'] = user_content.find('h2').string
		user_msg = user_content.find('div', class_ = re.compile(r'articleGender.*'))
		if user_msg:
			content_item['user_gender'] = user_msg['class'][1]
			content_item['user_age'] = user_msg.string
		else:
			content_item['user_gender'] = ''
			content_item['user_age'] = ''
		content_item['user_content'] = user_content.find('div', class_ = 'content').string
		img_url = user_content.find('img',src = re.compile(r'.*pictures.*'))
		if img_url:
			content_item['img_url'] = img_url['src']
		else:
			content_item['img_url'] = ''
		yield content_item