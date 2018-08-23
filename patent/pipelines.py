# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from zhuanli.items import ZlItem, DownurlItem

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        # from_crawler 系统函数,会从settings中通过get方法获取对应的配置信息
        return cls(
            mongo_uri= crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        #通过MongoClient()创建一个操作客户端,需要传入host地址,端口
        self.client = pymongo.MongoClient(self.mongo_uri,27017)
        #通过客户端获取Mongol数据库,没有就创建一个数据库
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        # 获取集合,并插入数据
        #  spider将item推送过来
        # dict 将 item 转成字典类型,mongo插入数据时是字典类型
        if isinstance(item,ZlItem):
            self.db["zhuanliColletion"].insert(dict(item))
        return item

    def clsoe_spider(self,spider):
        # 关闭客户端
        self.client.close()

class DownloadPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        applyNo = request.meta['anum']
        file_name = applyNo + '.pdf'
        return file_name

    def get_media_requests(self, item, info):
        # 生成Request请求,参数传入下载的url地址
        # item是爬取生成的Item对象

        if isinstance(item,DownurlItem):
            applyNo = item['applyNo']
            yield Request(item['downurl'],meta={'anum':applyNo})

    #以下可以有,可以无
    # def item_completed(self, results, item, info):
    #     #Item完成下载时的处理方法
    #     #results 是Item对应的下载结果.是一个list
    #     # image_paths = [x['path'] for ok, x in results if ok]
    #     # if not image_paths:
    #     #     raise DropItem('Document Downloaded Failed')
    #     return item



