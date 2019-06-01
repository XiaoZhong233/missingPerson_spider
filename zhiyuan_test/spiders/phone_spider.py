import scrapy

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    start_urls=[
        'http://www.jihaoba.com/escrow/'
    ]
#   response是下载器给爬虫的响应
    def parse(self, response):
        for ul in response.xpath('//div[@class="numbershow"]/ul'):
            phone=ul.xpath('li[contains(@class,"number hmzt")]/a/@href').re("\\d{11}")[0]
            price=ul.xpath('li[@class="price"]/span/text()').extract_first()[1:]

            if price.endswith('万'):
                price = int(float(price[:-1])*10000)
            #print(price)
            else:
                price = int(price)
            #输出数据
            yield {
                "phone": phone,
                "price": price
            }

        next='http://www.jihaoba.com'+response.xpath('//a[@class="m-pages-next"]/@href').extract_first()
        #需要转成绝对路径
        #爬虫分发给下载器下一次的任务，主要要异步操作
        #将next导入任务序列
        yield scrapy.Request(next)
