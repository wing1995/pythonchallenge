# -*- coding: utf-8 -*-

# Scrapy settings for xywy_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
#  设置所使用的数据处理管道以及mongodb连接参数和代理躲避爬虫被禁

BOT_NAME = 'xywy_crawl'

SPIDER_MODULES = ['xywy_crawl.spiders']
NEWSPIDER_MODULE = 'xywy_crawl.spiders'

# 设置等待时间缓解服务器压力 并隐藏自己
DOWNLOAD_DELAY = 1

RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1653.0 Safari/537.36'
# 配置使用的数据管道
ITEM_PIPELINES = ['xywy_crawl.pipelines.XywyCrawlPipeline']

MONGODB_SERVER = 'localhost'  # 这里都是默认的设置，不需要修改
MONGODB_PORT = 27017
MONGODB_DB = 'xywy_spider'
MONGODB_COLLECTION = 'spider'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xywy_crawl (+http://www.yourdomain.com)'

