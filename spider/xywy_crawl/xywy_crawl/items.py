# -*- coding: utf-8 -*-

'''
定义XywyCrawlItem，实现蜘蛛机器人的代码里返回XywyCrawlItem的实例，Scrapy会自动序列化并导出json

'''
import scrapy


class XywyCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    questionUrl = scrapy.Field()  # 疾病问答的链接
    question = scrapy.Field()  # 病人具体的问题
    analyse = scrapy.Field()  # 病人问题的分析
    suggestion = scrapy.Field()  # 病人问题的建议

