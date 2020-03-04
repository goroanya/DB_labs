from urllib.parse import urljoin

from scrapy.spiders import Spider, Request
from scrapy import Selector
from lxml import etree

from lab1.spiders import BaseSpider


class PortativSpider(BaseSpider, Spider):
    """Spider to grab headphones info from portativ.ua"""

    name = 'portativ'
    start_urls = ['https://portativ.ua/category_2271479.html?naznachenie_1245=184713']
    pages = 20

    def parse(self, response):
        links = Selector(response=response) \
                .xpath('//div[@class="cataloggrid-item-name-block"]/a/@href') \
                .getall()[:PortativSpider.pages]
        for link in links:
            yield Request(url=urljoin(response.url, link), callback=self.parse_headphones)

    def parse_headphones(self, response):
        selector = Selector(response=response)

        yield {
            'name': selector.xpath('//h1/a/text()').get(),
            'price': selector.xpath('//*[@itemprop="price"]/@content').get(),
            'image': selector.xpath('//img[@data-timolident="product-media-popup"]/@src').get(),
            'description': selector.xpath('normalize-space(//div[@class="description-info"])').get()
        }

    @staticmethod
    def create_xhtml_table():
        dom = etree.parse(PortativSpider.get_data_filename())
        xslt = etree.parse('transformation.xsl')
        transform = etree.XSLT(xslt)
        new_dom = transform(dom)
        with open('output/table.xhtml', 'w') as f:
            f.write(etree.tostring(new_dom, pretty_print=True).decode())
