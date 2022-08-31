""" Module to scrap the data of all the LEDs from given website """
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from LED_data_scrapper.items import ProductItem

class ProductsSpider(CrawlSpider):
    """
    Spider class for Product, here only scrapping LED data
    """

    name = "products"
    allowed_domains = ['pakistanistores.com', 'www.mega.pk', 'www.aysonline.pk']
    start_urls =[
        'https://pakistanistores.com/prices/home-appliances/led-tv-prices',
        ]
    custom_settings = {"FEEDS": {"output.json": {"format": "json"}}}

    le_product_details = LinkExtractor(restrict_xpaths=('//*[@class = "row search-ul"]/li/a'))

    le_next = LinkExtractor(
                            restrict_xpaths=('//*[@class=" active"]/following::a[1]'),
                            attrs=("data-href"))

    rule_product_details = Rule(link_extractor=le_product_details,
                                callback='parse_product_details',
                                follow=False)
    rule_next_page = Rule(link_extractor=le_next,
                          follow=True)
    rules = (
        rule_product_details,
        rule_next_page,
    )

    def parse_product_details(self, response):
        """ Parsing Image details """
        loader = ItemLoader(item= ProductItem(), response=response)
        self.parse_name(loader)
        self.parse_price(loader)
        self.parse_image_link(loader)
        self.parse_description(loader)
        loader.add_value('link', response.url)
        yield loader.load_item()

    def parse_name(self, loader):
        """ Parse name of LED """
        loader.add_xpath('name',
        '//h1[@class = "inline blockOnPhone"]/text()\
        | //*[contains(@class, "product_title")]/text()\
        | //*[@class = "product-title" ]/text()\
        ')

    def parse_description(self, loader):
        """ Parse description of LED """
        loader.add_xpath('description',
        '//*[@class = "woocommerce-product-details__short-description"]/ul/li/text()\
        | //*[@class = "woocommerce-product-details__short-description"]/ul/li/strong/text()\
        | //*[@class = "woocommerce-product-details__short-description"]/p/text()\
        | //*[@id = "divInfo"]/p/text()\
        | //*[contains(@class ,"item_desc")]/text()')

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
        '//*[contains(@class ,"img-responsive")]/@src\
        | //*[contains(@class,"wp-post-image")]/@src \
        | //*[@id ="mainImage"]/@src')
