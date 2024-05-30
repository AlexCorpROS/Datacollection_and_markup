import scrapy
from scrapy.http import HtmlResponse
from items import UnsplashItem
from scrapy.loader import ItemLoader
class UnspSpider(scrapy.Spider):
    name = "unsp"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response:HtmlResponse):
        links = response.xpath("//figure//a[@class='Prxeh']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_img)


    def parse_img(self, response:HtmlResponse):
        # name = response.xpath("//h1/text()").get()
        # url = response.url
        # photo = response.xpath("//button//div[@class='WxXog']/img/@src").get()
        # category = str(self.start_urls).split('/')[-1]
        # yield(UnsplashItem(name=name,url=url,photo=photo,category=category))

        loader = ItemLoader(item=UnsplashItem(),response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_value('category', str(self.start_urls).split('/')[-1])
        loader.add_xpath('photo', "//button//div[@class='WxXog']/img/@src")

        yield loader.load_item()




