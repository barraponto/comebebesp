# -*- coding: utf-8 -*-
from urlparse import urljoin

import scrapy
from scrapy.contrib.loader.processor import Identity, Compose, TakeFirst

from comebebesp.items import ComebebespItemLoader

def cleanup_city(city):
    if city.startswith('/ '):
        return city[2:]
    else:
        return city

class VejaspItemLoader(ComebebespItemLoader):
    telephone_out = Identity()
    city_out = Compose(TakeFirst(), cleanup_city)


class VejaspSpider(scrapy.Spider):
    name = "vejasp"
    allowed_domains = ["vejasp.abril.com.br"]
    root_url = 'http://vejasp.abril.com.br/'
    url_template = ('http://vejasp.abril.com.br/estabelecimento/busca'
                   '?per_page=20&page={page}&q=&fq=Restaurantes'
                   '&bairro=&nome=&preco_maximo=')


    def start_requests(self):
        return [scrapy.Request(self.url_template.format(page=1),
                               meta={'page': 1})]

    def parse(self, response):
        establishments = response.css('.map-list-item')
        for establishment in establishments:
            item_url = establishment.css(
                '.establishment-name a::attr("href")').extract()[0]

            loader = VejaspItemLoader(selector=establishment)
            loader.add_css('name', '.establishment-name::text')
            loader.add_css('address',
                           '.establishment-details p:first-child *::text')
            loader.add_css('neighborhood',
                           '[data-filtered-search-filter="bairro"]::text')
            loader.add_xpath('city',
                             '{xpath}/following-sibling::text()'.format(
                                 xpath=establishment._css2xpath(
                                     '[data-filtered-search-filter="bairro"]')))
            loader.add_css('category',
                           ('[data-filtered-search-filter="especialidades"]'
                            '::text'))

            yield scrapy.Request(urljoin(self.root_url, item_url),
                                 callback=self.parse_item,
                                 meta={'item': loader.load_item()})

        if establishments:
            next_page = response.meta['page'] + 1
            yield scrapy.Request(self.url_template.format(page=next_page),
                                 meta={'page': next_page})

    def parse_item(self, response):
        loader = VejaspItemLoader(item=response.meta['item'],
                                  response=response)
        loader.add_css('telephone', '.tel-number-protocol::text')
        loader.add_css('website', '.website a::attr("href")')
        return loader.load_item()

