import scrapy
from scrapy.loader import ItemLoader
from college_dunia.items import InstituteItem, CourseItem
from scrapy.selector import XmlXPathSelector
from college_dunia.models import InstitutesData
from college_dunia.pipelines import closestMatch, BasePipeline
import logging
from scrapy.utils.log import configure_logging

b = BasePipeline()
session = b.makeSession()

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

class XMLSpider(scrapy.Spider):
    name = "cdspider"
    allowed_domains = ["https://www.collegedunia.com", "collegedunia.com"]

    start_urls = ["http://collegedunia.com/engineering-colleges?ajax=1&page="+str(i) for i in range(1,2)]

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
        l.add_xpath( "website" , '//*[@id="renderTabData"]/div[15]/div/div/div[1]/div/div[3]/div/p/a/@href')
        l.add_xpath('address' ,'//*[@id="renderTabData"]/div[15]/div/div/div[1]/div/div[1]/div[1]/h3/text()')
        link = response.url + "/courses-fees"
        a = l.load_item()
        yield scrapy.Request(link, callback = self.parse_institute_course , meta = {"college":a})
        yield a

    def parse_institute_course(self, response):
        instituteItem = response.meta.get('college')
        college = InstitutesData(**instituteItem)
        matchInstitute = closestMatch(instituteItem.get('name'),session).get('d')

        #load the courses
        for part in response.xpath("//div[@class='content_body course_snipp_body']").extract():
            course = self.courseLoader(part)


        #Check if this course is added to this college in our database
        
        
        
