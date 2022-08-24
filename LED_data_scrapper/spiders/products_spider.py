""" Module to scrap the data of all the LEDs fromgiven website """
import scrapy
from scrapy.loader import ItemLoader
from LED_data_scrapper.items import ProductItem

class ProductsSpider(scrapy.Spider):
    """
    Spider class for Product, here only scrapping LED data
    """

    name = "products"

    start_urls = ['https://pakistanistores.com/prices/home-appliances/led-tv-prices', ]

    def parse(self, response):
        # pylint: disable=arguments-differ
        """ Parsing function """
        products = response.xpath('//ul[@class="row search-ul"]/\
                                li[@class="col-md-3 col-md-3 col-sm-6 col-xs-6"]')

        for product in products:
            loader = ItemLoader( item= ProductItem(), selector= product)
            loader.add_xpath('name', './/h5[@itemprop="name"]/text()')
            loader.add_xpath('link', './/a[@rel="nofollow"]/@href')
            loader.add_xpath('price', './/div[@class="primary-color price"]/text()')
            loader.add_xpath('image_link', './/img[@itemprop="image"]/@data-src')

            product_item = loader.load_item()
            product_url = product.xpath('.//a[@rel="nofollow"]/@href').get()
            # Scrap description of the product from next page
            yield response.follow(
                product_url,
                self.parse_product_details,
                meta={'product_item': product_item})

        pagination_links = response.xpath('//a[@class = "page-link navigate"]/@data-href').get()
        for anchor in pagination_links:
            new_url = response.urljoin (anchor)
            yield response.follow(new_url, callback = self.parse)  # To scrap Next pages

    def parse_product_details(self, response):
        """ Parsing Image details """
        product_item = response.meta['product_item']
        loader = ItemLoader(item= product_item, response=response)
        loader.add_xpath('description',
        '//div[@class = "woocommerce-product-details__short-description"]/ul/li/text()\
        | //div[@class = "woocommerce-product-details__short-description"]/ul/li/strong/text()\
        | //div[@id = "divInfo"]/p/text()\
        | //p[@class = "item_desc text-justify margint-20"]/text()')

        yield loader.load_item()
