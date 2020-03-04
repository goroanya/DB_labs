from lxml import etree
from scrapy import exceptions, Selector, Spider, Request
from urllib.parse import urljoin

from lab1.spiders import BaseSpider


class ISportSpider(BaseSpider, Spider):
    """Spider to grab all text and images from bigmir.net"""

    name = 'isport'
    start_urls = ['https://isport.ua/']
    allowed_domains = ['isport.ua']
    pages_max = 20

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visited_pages = []

    def _check_stop_criteria(self):
        if len(self.visited_pages) >= self.pages_max:
            raise exceptions.CloseSpider('Maximum visited pages number exceeded')

    def parse(self, response):
        self._check_stop_criteria()

        if response.url not in self.visited_pages:
            self.visited_pages.append(response.url)
            yield self.parse_url(response)

        urls = Selector(response=response).xpath('//a/@href').getall()
        for url in urls:
            yield Request(url=urljoin(response.url, url), callback=self.parse)

    def parse_url(self, response):
        selector = Selector(response=response)

        text_data = selector \
            .xpath('//div[@id="article_content"]//text() | //div[@class="article__title"]//text()').getall()
        images = selector \
            .xpath('//img/@src').getall()

        return {
            'url': response.url,
            'text_data': [t.strip() for t in text_data],
            'images': [response.urljoin(src) for src in images]
        }

    @classmethod
    def get_all_urls(cls):
        return etree.parse(cls.get_data_filename()) \
            .xpath('page/@url')
