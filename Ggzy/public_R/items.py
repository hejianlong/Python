# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PublicRItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field() # 标题
    stage = scrapy.Field() # 招投、中标状态
    itemNo = scrapy.Field() # 采购项目编号 暂不采集
    content = scrapy.Field() # 内容页
    pub_time = scrapy.Field() # 发布时间
    province = scrapy.Field() # 省
    source_url = scrapy.Field() # 来源链接
    media_file = scrapy.Field() # 文件路径
    source_name = scrapy.Field()
    key = scrapy.Field()
    category = scrapy.Field()