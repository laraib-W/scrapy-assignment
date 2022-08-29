""" Module to scrap the data of all the LEDs from given website """
import scrapy
from scrapy.loader import ItemLoader
from LED_data_scrapper.items import ProductItem

class ProductsSpider(scrapy.Spider):
    """
    Spider class for Product, here only scrapping LED data
    """

    name = "products"
    custom_settings = {"FEEDS": {"results.json": {"format": "json"}}}

    def start_requests(self):
        return [scrapy.Request('https://pakistanistores.com/prices/home-appliances/led-tv-prices',
                                   callback=self.parse)]

    def parse(self, response):
        # pylint: disable=arguments-differ
        """ Parsing function for products """
        products = response.xpath('//*[@class="col-md-3 col-md-3 col-sm-6 col-xs-6"]')

        for product in products:
            loader = ItemLoader( item= ProductItem(), selector= product)
            self.parse_link(loader)
            product_item = loader.load_item()
            product_url = product.xpath('.//*[@rel="nofollow"]/@href').get()
            # Scrap details of the product from the product detail page
            yield response.follow(
                product_url,
                self.parse_product_details,
                meta={'product_item': product_item})

        pagination_links = response.xpath('//*[@class = "page-link navigate"]/@data-href').getall()
        for anchor in pagination_links:
            new_url = response.urljoin (anchor)
            yield response.follow(new_url, callback = self.parse)  # To scrap Next pages


    def parse_product_details(self, response):
        """ Parsing Image details """
        product_item = response.meta['product_item']
        loader = ItemLoader(item= product_item, response=response)
        self.parse_name(loader)
        self.parse_price(loader)
        self.parse_image_link(loader)
        self.parse_description(loader)
        yield loader.load_item()

    def parse_link(self,loader):
        """ Parse link of LED details page """
        loader.add_xpath('link', './/*[@rel="nofollow"]/@href')

    def parse_name(self, loader):
        """ Parse name of LED """
        loader.add_xpath('name',
        '//*[@class = "inline blockOnPhone"]/text()\
        | //*[@class = "product_title entry-title wd-entities-title"]/text()\
        | //*[@class = "product-title" ]/text()\
        ')

    def parse_description(self, loader):
        """ Parse description of LED """
        loader.add_xpath('description',
        '//*[@class = "woocommerce-product-details__short-description"]/ul/li/text()\
        | //*[@class = "woocommerce-product-details__short-description"]/ul/li/strong/text()\
        | //*[@class = "woocommerce-product-details__short-description"]/p/text()\
        | //*[@id = "divInfo"]/p/text()\
        | //*[@class = "item_desc text-justify margint-20"]/text()')

    def parse_price(self, loader):
        """ Parse price of each LED """
        loader.add_xpath('price',
        '//*[@class = "newPrice inline blockOnPhone"]/text()\
        |//*[@class = "summary-inner"]/*[@class = "price"]/ins/*[@class = "woocommerce-Price-amount amount"]/bdi/text()\
        |(//*[@class = "summary-inner"]/*[@class = "price"]/*[@class = "woocommerce-Price-amount amount"]/bdi/text())[2]\
        |//*[@id = "price"]/text()')

    def parse_image_link(self, loader):
        """ Parse image link of each LED """
        loader.add_xpath('image_link',
        '//*[@class = "img-responsive padding-10 center-block"]/@src\
        | //*[@class = "wp-post-image wp-post-image"]/@src \
        | //*[@id ="mainImage"]/@src')

    def parse_next_pages(self, response):
        """ To parse Next pages of the website """
        pagination_links = response.xpath('//a[@class = "page-link navigate"]/@data-href').getall()
        for anchor in pagination_links:
            new_url = response.urljoin (anchor)
            yield response.follow(new_url, callback = self.parse)  # To scrap Next pages
