import scrapy


#更改搜索路径，但没有用哦
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)




class MissingSpider(scrapy.Spider):
    name = 'personUrl'
    start_urls = [
       "https://bbs.baobeihuijia.com/forum-191-1.html"
    ]

    def parse(self, response):
        for table in response.xpath('//table[contains(@id,"threadlisttableid")]'):
            #detailUrl = "https://bbs.baobeihuijia.com/"+th.xpath('a[@class="s xst"]/@href').extract_first()
            #uri = th.xpath('a[contains(@class,"number hmzt")]/a/@href').re("\\d{11}")[0]
            #detailUrl =th.xpath('a[@class="s xst"]/@href').extract_first()
            detailUrl = table.xpath('//a[@class="s xst"]/@href').extract()

        urlitems =[]
        for url in detailUrl:
            #print("https://bbs.baobeihuijia.com/"+url)
            #urlitems.append("https://bbs.baobeihuijia.com/"+url)
            #产生格式化数据
            from urlItem import urlItem
            murl = urlItem()
            murl["url"] = "https://bbs.baobeihuijia.com/"+url
            print(url)
            yield murl

            yield {
                "detailUrl": "https://bbs.baobeihuijia.com/"+url
            }
        pass

        #print(len(urlitems))






