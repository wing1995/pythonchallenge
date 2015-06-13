# -*- coding: utf-8 -*-

import re
import urllib2
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from xywy_crawl.items import XywyCrawlItem
from scrapy import log


class XywySpider(CrawlSpider):
	name = 'xywy_spider'  # 定义爬虫的名字
	allowed_domains = ['club.xywy.com']  # 爬取的主要范围
	# 搜集2014年每一天的链接
	page_urls = 'http://club.xywy.com/keshi/%d.html'   # 寻找2014年所在的每一个网站
	range = [1]  # 测试代码，先爬一页的数据
	# range = [1,2,3,4,5,6]  # 一共有6个页面有2014年的数据
	start_urls = []  # 初始化初始页面
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
	                         ' Chrome/39.0.2171.99 Safari/537.36'}  # 伪装成浏览器访问
	for page_index in range:  # 开始遍历每一个页面
		page_url = page_urls % page_index
		request = urllib2.Request(url=page_url, headers=headers)  # 创建一个请求
		response = urllib2.urlopen(request)  # 打开请求
		html = response.read().decode('gb2312')  # 转码
		# 找到该页面下的2014年所有链接
		all_dates_link = re.findall(r'(?<=href=["])http://club.xywy.com/keshi/2014-\d{2}-\d{2}/1.html(?=["])', html)
		for each_date_link in all_dates_link:
			start_urls.append(each_date_link)
			pass
		pass

	rules = [
		# 找到日期链接下的页面中问答链接中具体内容如‘http://club.xywy.com/static/20141231/59863952.htm’,并且采用callback里面的函数对问答链接里面的网页进行访问
		Rule(SgmlLinkExtractor(allow=('static/\d{8}/[^/]+(\.htm)$'),), callback='post_parse'),
		# 找到下一页的链接内容如'http://club.xywy.com/keshi/2014-12-25/1.html'
		Rule(SgmlLinkExtractor(allow=('keshi/\d{4}-\d{2}-\d{2}/\d+\.html'),), follow=True),
	]

	def post_parse(self, response):
		x = Selector(response)  # 选择给定的网页源代码
		item = XywyCrawlItem()  # 实例化item对象
		items = []  # 初始化每条记录

		item['questionUrl'] = response.url  # 所有的问答链接
		item['question'] = ""  # 病人具体的问题，有些是只有描述没有问题的
		item['analyse'] = ""  # 疾病问题的分析
		item['suggestion'] = ""  # 疾病问题的建议

		str_list = x.select('//div[@class="graydeep User_quecol pt10 mt10"]/text()').extract()  # 提取问题
		if len(str_list) == 1:
			item['question'] = str_list[0]  # 取第1个字符串
		elif len(str_list) == 2:
			item['question'] = str_list[1]  # 取第2个字符串
		else:
			str_list = x.select('//h2/p[@class="fl dib fb"]/text()').extract()  # 如果找不到问题，就用描述替代问题
			item['question'] = str_list[0]

		str_list = x.select('//div[@class="pt15 f14 graydeep  pl20 pr20"]/text()').extract()  # 提取问题的答案
		if len(str_list) > 1:
			item['analyse'] = str_list[0].encode("utf-8")  # 第一个字符串是分析
			item['suggestion'] = str_list[1].encode("utf-8")  # 第二个字符串是建议
		elif len(str_list) == 1:  # 有些是只有分析的
			item['analyse'] = str_list[0].encode("utf-8")  # 第一个字符串是分析

		log.msg(item['questionUrl']+'   '+item['question'])  # 记录到日志里面
		print item  # 在命令行下观察爬虫的踪迹
		items.append(item)
		return items