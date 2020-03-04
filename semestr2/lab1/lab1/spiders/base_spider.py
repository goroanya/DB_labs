import os

class BaseSpider:
    """All spiders ancestor with common methods"""
    name = 'base'

    @classmethod
    def get_data_filename(cls):
        """
        @return: data file name depending on spider's name
        """
        return f'output/{cls.name}.xml'

    @classmethod
    def run(cls):
        """
        Run scrapy script for crawling with this spider
        """
        os.system(f'scrapy crawl {cls.name}')
