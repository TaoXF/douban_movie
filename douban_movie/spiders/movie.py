# -*- coding: utf-8 -*-
import scrapy
import json
import time

import logging; logger = logging.getLogger(__name__)

from redis_db import redis_db

from scrapy import Request

from douban_movie.items import DoubanMovieItem


class MovieSpider(scrapy.Spider):
	name = 'movie'
	allowed_domains = ['movie.douban.com']
	start_urls = ['http://movie.douban.com/']
	start_time = None
	repeat_count = 0

	def start_requests(self):
		self.start_time = int(time.time())
		url = redis_db.pop_movie_url()
		while url:
			url = redis_db.pop_movie_url()
			yield Request(url, callback=self.parse)

	def parse(self, response):
		datas = json.loads(response.text).get('data')
		logger.info("request successful")
		for data in datas:
			item = DoubanMovieItem()
			for field in item.fields:
				if field in data:
					item[field] = data[field]
			id = item['movie_id'] = data['id']
			if redis_db.add_movie_id(id):
				# logger.info('add %s in redis' %data['title'])
				yield item
			else:
				self.repeat_count += 1

	def closed(self, reason):
		crawl_time = int(time.time()) - self.start_time
		logger.info("抓取时间共计 %s" %crawl_time)
		logger.info("重复数量共计 %s" %self.repeat_count)
