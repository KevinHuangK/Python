# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()  # 类型 3.Boss直聘
    ename = scrapy.Field()  # 公司名称
    postinfo = scrapy.Field()  # 岗位信息
    salary = scrapy.Field()  # 薪资
    oldurl = scrapy.Field()  # 原始url
    releasetime = scrapy.Field()  # 招聘信息发布时间
