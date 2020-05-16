# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class HotlineSpider(scrapy.Spider):
    name = 'hotline'
    allowed_domains = ['www.hotline.ua']
    start_urls = ['https://hotline.ua/mobile/mobilnye-telefony-i-smartfony/']

    def parse(self, response: Response):
        products = response.xpath("//li[contains(@class, 'product-item')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//div[@class='item-info']/p[@class='h4']/a/text()").get(),
                'price': product.xpath(".//span[@class='value']/text()").get(),
                'img': product.xpath(".//img[@class='img-product']/@src").get()
            }