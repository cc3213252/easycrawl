# -*- coding: utf-8 -*-
import scrapy
from easycrawl.items import EasycrawlItem


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]
    allowd_domains = [
        'toscrape.com'
    ]


    def parse(self, response):
        for quote in response.css("div.quote"):
            item = EasycrawlItem()
            item['text'] = quote.css("span.text::text").extract_first()
            item['author'] = quote.css("small.author::text").extract_first()
            item['tags'] = quote.css("div.tags > a.tag::text").extract()
            author_page = response.css('small.author+a::attr(href)').extract_first()
            item['author_full_url'] = response.urljoin(author_page)
            yield scrapy.Request(url=item['author_full_url'], meta={'item': item}, callback=self.parse_author, dont_filter=True)

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            next_full_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_full_url, callback=self.parse)


    def parse_author(self, response):
        item = response.meta['item']
        item['author_born_date'] = response.css('.author-born-date::text').extract_first()
        item['author_born_location'] = response.css('.author-born-location::text').extract_first()
        item['author_description'] = response.css('.author-born-location::text').extract_first()
        yield item


