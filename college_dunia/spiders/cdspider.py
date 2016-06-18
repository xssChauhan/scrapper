import scrapy
from scrapy.loader import ItemLoader
from college_dunia.items import InstituteItem

import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    filemode = 'a',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)


class CDSpider(scrapy.Spider):
    name = "cdspider"
    allowed_domains = ["http://www.collegedunia.com", "collegedunia.com"]

    start_urls = ["http://collegedunia.com/pharmacy/solan-colleges"]

    def parse(self, response):
        for link in response.css("a.college_name::attr('href')"):
            l = response.urljoin(link.extract())
            print(l)
            yield scrapy.Request(l ,self.parse_institute)

    def parse_institute(self,response):
        print("calling parse_institute")
        l = ItemLoader(item = InstituteItem() , response = response)
        l.add_css( 'name' , "h1#page_h1::text" )
        l.add_value('status' , "s")
        l.add_xpath("website" , "//div[@class='web_block']/div/p/a/@href" )
        l.add_xpath('founded_in' , "//div[@class='college_data']/div[@class='extra_info']/span[last()]/text()")
        #l.add_xpath('facilities' , "//div[@class='facility']/span[@class='facility_name']/text()")
        l.add_xpath("about","//div[@class='container-fluid about-article']//div[@class='content_p']/p[1]/text()")
        l.add_xpath('address' ,"//div[@class='address row']//h3/text()")
        return l.load_item()
