# -*- coding: utf-8 -*-
import scrapy

# 根据html标签获取标签内容
# cmd到scrapy.cfg所在的目录，如（E:\Study\Python\Scrapy\tutorial）
# scrapy crawl toscrape-css
# scrapy crawl toscrape-css -o toscrape-css.json

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

