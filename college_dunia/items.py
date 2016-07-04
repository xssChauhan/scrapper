# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags
import re
from college_dunia.helpers import getYears

def enter_filter(item):
    return item.replace("\n"," ")

def stupid_filter(item):
    print(item)
    return item[0].replace(u'\xa0', u' ')

def stupid_filter_father(item):
    return stupid_filter(item[0])

def ascii_filter(item):
    return item[0].decode('unicode_escape').encode('ascii','ignore')


class InstituteItem(Item):
    name = Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join()
    )
    status = Field(output_processor = Join())
    website = Field( output_processor = Join())
    address = Field(
                input_processor = MapCompose( remove_tags , enter_filter),
                output_processor = Join()
    )

class CourseItem(Item):
    name = Field(output_processor = Join())
    #level = Field()
    duration = Field(
        input_processor = getYears,
        output_processor = Join() )
    # subcourses = Field()
    # seats = Field()
    # fees = Field()

class CourseLevel(Item):
    name = Field()

class SubcourseItem(Item):
    name = Field()