# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2,datetime

class PublicRPipeline(object):
    def __init__(self):
        self.table = 'spider_info_01'
        self.host = 'localhost'
        self.database = 'ddb'
        self.user = 'spideruser'
        self.password = '*****'
        self.port = '5432'

    def open_spider(self, spider):
            self.db = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            self.cursor = self.db.cursor()

    def close_spider(self,spider):
        self.db.close()
        self.cursor.close()

    def process_item(self, item, spider):
        self.db.commit()
        item['key'] = '招投标'
        item['category'] = '03'
        item['content'] = item['content'].replace('\'', '\"')
        if not item['pub_time']:
            item['pub_time'] = str(datetime.datetime.now())
        if item['content']: # 如果当前信息为空，则不添加
            data = dict(item)
            keys = ','.join(data.keys())
            try:
                sql = r'insert into %s(%s) values%s' % (self.table, keys, tuple(data.values()))
                self.cursor.execute(sql)
                self.db.commit()
                print('存储数据中....', item['title'])
            except Exception as e:
                print('数据已存在', e)

