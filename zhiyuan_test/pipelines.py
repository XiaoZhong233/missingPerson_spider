# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#更改搜索路径，但没有用哦
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pymysql.cursors
from scrapy.conf import settings
from twisted.enterprise import adbapi

#该方法支持异步
class DBHelper():
    def __init__(self):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

        # 插入数据
    def insert(self, item):
        from PersonItem import PersonItem
        if isinstance(item, PersonItem):

            tb_name=settings['MYSQL_TABLE']


            # sql = """insert into missingperson(missingperson.`name`, sex, birth, tall ,adress,cor,missingperson.`describe`,other,update_time,imgurl)
            #                     value (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"""
            # 这里定义要插入的字段           #后面加更新语句
            #
            # sql = """insert into """ + tb_name + """(""" + tb_name + """.`name`, sex, birth, tall ,adress,cor,""" + tb_name + """.`describe`,other,update_time,imgurl,missingdate) value (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            #              missingdate = """ + "\"" + item['missingdate'] + "\""

            sql = """insert into """ + tb_name + """(""" + tb_name + """.`name`, sex, birth, tall ,adress,cor,"""+tb_name+""".`describe`,other,update_time,imgurl,missingdate) value (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s) """
            #print(sql);
            # 调用插入的方法
            query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
            # 调用异常处理方法
            query.addErrback(self._handle_error)
        # from zhiyuan_test.zhiyuan_test.spiders.missingPersonUrl_spider import urlItem
        from urlItem import urlItem
        if isinstance(item,urlItem):
            sql = "insert into url(url) value(%s)"
            # 调用插入的方法
            query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
            # 调用异常处理方法
            query.addErrback(self._handle_error)
        return item

        # 写入数据库中
    def _conditional_insert(self, canshu, sql, item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来存入items内的数据
        from PersonItem import PersonItem
        if isinstance(item,PersonItem):
            import datetime
            params = (item['name'], item['sex'],item['birth'],item['tall'],item['adress'],item['cor'],item['describe'],item['other'],datetime.datetime.now(),item['imgsrc'],item['missingdate'])
            canshu.execute(sql, params)

        from urlItem import urlItem
        if isinstance(item,urlItem):
            params = (item['url'])
            canshu.execute(sql,params)

        # 错误处理方法
    def _handle_error(self, failue):
        pass
        print('--------------database operation exception!!-----------------')
        #回滚
        #self.connect.rollback()
        #print(failue)


class ZhiyuanTestPipeline(object):
    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        # 插入数据库
        self.db.insert(item)
        return item

