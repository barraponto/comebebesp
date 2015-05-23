# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from comebebesp.items import ComebebespItemLoader


class BaresspSpider(CrawlSpider):
    name = 'baressp'
    allowed_domains = ['baressp.com.br']
    start_urls = [
        'http://www.baressp.com.br/bares/pesquisa/?FC=1'
    ]

    rules = (
        # Follow next pages rule.
        Rule(LinkExtractor(restrict_css='#paginacao a'),
             follow=True),
        # Visit every item rule.
        Rule(LinkExtractor(restrict_css='#listaBusca a.titulo'),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        loader = ComebebespItemLoader(response=response)
        loader.add_css('name', '[itemprop="name"]')
        loader.add_css('address', '[itemprop="street-address"]')
        loader.add_css('city', '[itemprop="locality"]')
        loader.add_css('telephone', '[itemprop="tel"]')
        loader.add_css('website', '[itemprop="url"]')
        loader.add_css('category', ('#arvoredenavegacao li:first-child '
                                    'a:last-child::text'))
        return loader.load_item()
