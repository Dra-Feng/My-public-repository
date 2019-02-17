# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanSpider'
    ##allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']
    start = 0 # 设置一个变量规律每增加25就是往下翻一页
    url = 'https://movie.douban.com/top250?start='
    end = '&filter='
    start_urls = [url + str(start) + end]

    def parse(self, response):
        # 实例化item类
        item = DoubanItem()

        # 找出每部电影总的div 并进行遍历 再取详细信息
        for each in response.xpath("//div[@class='info']"):
            title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            content = each.xpath('div[@class="bd"]/p/text()').extract()
            score = each.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            info = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

            item['title'] = title[0]
            item['content'] = content[0]
            item['score'] = score[0]
            item['info'] = info

            yield item

            # 排行榜共250条 每25条一页
            if self.start <= 225:
                self.start += 25
                url = self.url + str(self.start) + self.end
                yield scrapy.Request(url,callback=self.parse)
