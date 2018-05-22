# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field


class DoubanMovieItem(scrapy.Item):
	_id = Field()
	url = Field()
	rate = Field()
	title = Field()
	cover = Field()
	casts = Field()
	movie_id = Field()
	directors = Field()



