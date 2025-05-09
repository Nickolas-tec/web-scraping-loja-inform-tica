import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["www.saldaodainformatica.com.br"]
    start_urls = ["https://www.saldaodainformatica.com.br/notebook"]
    page_count = 1
    max_page = 10


    def parse(self, response):

        produtos =  response.css('div.js-product.product.col-xs-12.col-sm-6.col-xl-4')

        for produto in produtos:
            yield{
                'produto': produto.css('h2.h3.product-title a::text').get(),
                'preco_antigo': produto.css('span.z-preco-antigo::text').get(),
                'preco_final': produto.css('p.preco-final::text').get()
            }
        if self.page_count < self.max_page:
          next_page = response.css('li a.next.js-search-link::attr(href)').get()
          if next_page:
              self.page_count += 1
              yield scrapy.Request(url=next_page, callback=self.parse)
          pass
