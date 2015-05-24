# -*- coding: utf-8 -*-
from purl import URL
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import Identity, MapCompose, TakeFirst

from comebebesp.items import ComebebespItemLoader

def facebook_link_filter(href):
    if 'facebook' in href:
        return URL(href).query_param('URL')

def twitter_link_filter(href):
    if 'twitter' in href:
        return URL(href).query_param('URL')


class BaresspItemLoader(ComebebespItemLoader):
    telephone_out = Identity()
    email_out = Identity()
    facebook_out = MapCompose(facebook_link_filter, TakeFirst())
    twitter_out = MapCompose(twitter_link_filter, TakeFirst())


class BaresspSpider(CrawlSpider):
    name = 'baressp'
    allowed_domains = ['baressp.com.br']
    start_urls = [
        'http://www.baressp.com.br/bares/pesquisa/?FC=1',
        'http://www.baressp.com.br/bares/pesquisa/?FC=2'
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
        loader = BaresspItemLoader(response=response)
        loader.add_css('name', '[itemprop="name"]')
        loader.add_css('address', '[itemprop="street-address"]')
        loader.add_css('city', '[itemprop="locality"]')
        loader.add_css('telephone', '[itemprop="tel"]')
        loader.add_css('website', '[itemprop="url"]')
        loader.add_css('facebook', '.texto [target]::attr("href")')
        loader.add_css('twitter', '.texto [target]::attr("href")')
        loader.add_css('email', ('#estabelecimento_informacoes '
                       '[href^="mailto"]'))
        loader.add_css('category', ('#arvoredenavegacao li:first-child '
                                    'a:last-child::text'))
        return loader.load_item()
