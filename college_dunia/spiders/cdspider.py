import scrapy
from scrapy.loader import ItemLoader
from college_dunia.items import InstituteItem, CourseItem
from scrapy.selector import XmlXPathSelector
from college_dunia.models import InstitutesData
from college_dunia.pipelines import closestMatch, BasePipeline,session
from college_dunia.helpers import DateParse, newResponse
import logging
from scrapy.utils.log import configure_logging
from datetime import datetime


configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    filemode = 'a',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)

avoid = ["rankings" , "gallery" , "contact"]

def addCourseRequest(url):
    yield scrapy.Request(url , self.parse_institute_course)

class CDSpider(scrapy.Spider):
    name = "cdspider"
    allowed_domains = ["https://www.collegedunia.com", "collegedunia.com"]

    #engg = ["http://collegedunia.com/engineering-colleges?ajax=1&page="+str(i) for i in xrange(1,379)]
    comm = ["http://collegedunia.com/commerce-colleges?ajax=1&page="+str(i) for i in xrange(1,270)]
    arts = ["http://collegedunia.com/art-colleges?ajax=1&page="+str(i) for i in xrange(1,320)]
    medical = ["http://collegedunia.com/medical-colleges?ajax=1&page="+str(i) for i in xrange(1,98)]
    management = ["http://collegedunia.com/management-colleges?ajax=1&page="+str(i) for i in xrange(1,449)]
    start_urls = medical + arts + comm
    def courseLoader(self,response):
        c = ItemLoader( item = CourseItem() , response = response )
        c.add_xpath("name" , "//span[@class='course_name']/text()")
        c.add_xpath("seats" , "//span[@class='course_info seats']/text()")
        c.add_xpath("fees" ,"//span[@class='fees']/text()")

        print c.load_item()


    def parse(self, response):
        for link in response.xpath("//div[@class='college_info']/a/@href").extract():
            yield scrapy.Request(link , self.parse_institute)
            #yield scrapy.Request(link + "/courses-fees" , callback = self.parse_institute_course )

    def parse_institute(self,response):
        l = ItemLoader(item = InstituteItem() , response = response)
        l.add_xpath( 'name' , "//h1[@class='college_name']/text()")
        l.add_value( 'status' , "s")
        l.add_xpath( "website" , "//div[@class='web_block']//p[@class='lr_detail']/a/@href")
        l.add_xpath('address' ,'//div[@class="loc_block"]//h3/text()')
        l.add_xpath('facilities',"//span[@class='facility_name']/text()")
        link = response.url + "/courses-fees"
        a = l.load_item()
        yield scrapy.Request(link, callback = self.parse_institute_course , meta = {"college":a})
        yield a

    def parse_institute_course(self, response):
        instituteItem = response.meta.get('college')
        matchInstitute = closestMatch(instituteItem.get('name')).get('d')
        if matchInstitute is None : print "From Pipeline , Match institute", matchInstitute," ", instituteItem.get("name")

        #load the courses
        for part in response.xpath("//div[@class='course_snipp_body']").extract():
            newR = newResponse(response,part)
            l = ItemLoader(item = CourseItem() , response = newR)
            l.add_xpath("name" , "//a[@class='course_name']/text()")
            l.add_xpath("duration","//span[@class='course_info duration-yr']/text()")
            l.add_xpath("subcourses","//a[@class='stream_tag']/text()")
            l.add_xpath("fee","//span[@class='fees']/text()")
            l.add_value("institute",{"i" : matchInstitute })
            a = l.load_item()
            yield a
