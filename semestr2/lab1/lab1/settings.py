"""Module with general scrapy settings"""
BOT_NAME = 'lab1'

SPIDER_MODULES = ['lab1.spiders']
NEWSPIDER_MODULE = 'lab1.spiders'


# Configure item pipelines
ITEM_PIPELINES = {
   'lab1.pipelines.XMLPipeline': 300,
}
