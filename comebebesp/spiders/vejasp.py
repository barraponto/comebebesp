# -*- coding: utf-8 -*-
import scrapy
from comebebesp.items import ComebebespItemLoader

class VejaspItemLoader(ComebebespItemLoader):
    pass


class VejaspSpider(scrapy.Spider):
    name = "vejasp"
    allowed_domains = ["vejasp.abril.com.br"]
    urltemplate = ('http://vejasp.abril.com.br/estabelecimento/busca'
                   '?per_page=20&page={page}&q=&fq=Restaurantes'
                   '&bairro=&nome=&preco_maximo=')


    def start_requests(self):
        return [scrapy.Request(self.urltemplate.format(page=1),
                               meta={'page': 1})]

    def parse(self, response):
        establishments = response.css('.map-list-item')
        for establishment in establishments:
            loader = VejaspItemLoader(selector=establishment)
            loader.add_css('name', '.establishment-name::text')
            loader.add_css('address', '.establishment-details p:first-child *::text')
            loader.add_css('neighborhood', '[data-filtered-search-filter="bairro"]::text')
            loader.add_xpath('city',
                             establishment._css2xpath('[data-filtered-search-filter="bairro"]') + '/following-sibling::text()')
            loader.add_xpath('telephone',
                             establishment._css2xpath('.label') + '/following-sibling::text()')
            loader.add_css('category', '[data-filtered-search-filter="especialidades"]::text')
            yield loader.load_item()
        if establishments:
            next_page = response.meta['page'] + 1
            yield scrapy.Request(self.urltemplate.format(page=next_page), meta={'page': next_page})
