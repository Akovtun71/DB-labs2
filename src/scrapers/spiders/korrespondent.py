# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class KorrespondentSpider(scrapy.Spider):
    name = 'korrespondent'
    allowed_domains = ['korrespondent.net']
    start_urls = ['https://korrespondent.net/ukraine/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'http')]")
        all_text = response.xpath("//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")
        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': image.get()} for image in all_images]
        }
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., 'https://korrespondent.net/')][substring(., string-length() - 4) = '.html']")
            selected_links = [link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)
