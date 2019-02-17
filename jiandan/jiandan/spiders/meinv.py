# -*- coding: utf-8 -*-
import scrapy
from jiandan.items import JiandanItem
from scrapy.crawler import CrawlerProcess


class MeinvSpider(scrapy.Spider):
    name = 'meinv'
    allowed_domains = ['http://jiandan.net/ooxx']
    start_urls = ['http://http://jiandan.net/ooxx/']

    def parse(self, response):
        item = JiandanItem()
        item['image_urls'] = response.xpath('//img//@src').extract() #提取图片链接
        yield item
        new_url = response.xpath('//a[@class="previous-comment-page'']//@href').extract_first() # 翻页
        if new_url:
            yield scrapy.Request(new_url,callback=self.parse)