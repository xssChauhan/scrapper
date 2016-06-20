import scrapy
from scrapy.loader import ItemLoader
from college_dunia.items import InstituteItem
from scrapy.selector import XmlXPathSelector

import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    filemode = 'a',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)

avoid = ["rankings" , "gallery" , "contact"]

class XMLSpider(scrapy.Spider):
    name = "fxmlspider"
    allowed_domains = ["https://www.collegesearch.in", "collegesearch.in"]

    start_urls = [ "https://www.collegesearch.in/Sitemap_cs_1.xml"]

    def parse(self, response):
        xxs = XmlXPathSelector(response = response)
        xxs.remove_namespaces()
        for link in xxs.xpath("/urlset/url/loc/text()"):
            l = link.extract()
            ls = l.split("/")[len(l.split("/")) - 1]
            if ls not in avoid:
                l = response.urljoin(link.extract())
                if ls != "courses":
                    yield scrapy.Request(l , self.parse_institute)
                else:
                    pass
                    #yield scrapy.Request(l , self.parse_institute_course)
                
            #yield scrapy.Request(l ,self.parse_institute)

    def parse_institute(self,response):
        l = ItemLoader(item = InstituteItem() , response = response)
        l.add_css( 'name' , "h3.clg-name-head strong::text" )
        l.add_value('status' , "s")
        l.add_css("website" , "div.col-md-4:nth-child(3) > div:nth-child(1) > span:nth-child(3)::text" )
        #l.add_xpath('founded_in' , "//div[@class='college_data']/div[@class='extra_info']/span[last()]/text()")
        #l.add_xpath('facilities' , "//div[@class='facility']/span[@class='facility_name']/text()")
        #l.add_xpath("about","//div[@class='container-fluid about-article']//div[@class='content_p']/p[1]/text()")
        l.add_css('address' ,"div.font12:nth-child(2)::text")
        return l.load_item()
