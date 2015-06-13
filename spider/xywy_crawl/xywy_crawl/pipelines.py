# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class XywyCrawlPipeline(object):
	def __init__(self):
		'''记住在执行scrapy之前要开启数据库的服务器，才能链接到mongodb'''
		self.server = settings['MONGODB_SERVER']  # 连接settings里面的参数，从而链接数据库的服务器
		self.port = settings['MONGODB_PORT']  # 链接数据的端口
		self.db = settings['MONGODB_DB']  # 链接数据的名字
		self.col = settings['MONGODB_COLLECTION']  # 链接数据的集合
		connection = pymongo.Connection(self.server, self.port)
		db = connection[self.db]
		self.collection = db[self.col]

	def process_item(self, item, spider):
		'''以字典的形式插入数据'''
		self.collection.insert(dict(item))
		log.msg('item written into mongodb database %s/%s' % (self.db, self.col), level=log.DEBUG)
		return item
