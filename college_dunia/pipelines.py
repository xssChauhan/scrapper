# -*- coding: utf-8 -*-
from sqlalchemy import or_
from models import *
from college_dunia.items import InstituteItem, CourseItem
import re,inspect
from college_dunia.PipelineTools import PipelineTools
from college_dunia.Session import session
from scrapy.exceptions import DropItem
from .helpers import DateParse


class InstituteDBPipeline():
    def process_item(self, item, spider):
        print "*************************************"
        if isinstance(item , InstituteItem):
            match =  PipelineTools.closestMatch(item.get('name') )
            if match.get('s') > 50 and match.get('d') is not None:
                #Process the institute and find the data that is missing in our database from the scraped page and add it to the database
                #processing the facilities and companies for now
                institute = match.get('d')
                institute.setFacilities(item.get('facilities') or []).setCompanies(item.get('companies') or [])
                institute = PipelineTools.makeInstituteObject(item,institute)
                try:
                    session.commit()
                    session.add(CrawlChange(table_name = institute.__tablename__,modification = "changed", entity = institute.id))
                except:
                    session.rollback()
            else:
                print "Adding To Database" + item.get('name')
                try:
                    institute = PipelineTools.makeInstituteObject(item)
                    session.add(institute)
                    institute.setFacilities(item.get('facilities') or []).setCompanies(item.get('companies')  or [])
                    session.commit()
                    session.add(CrawlChange(table_name = institute.__tablename__,modification = "new",entity = institute.id))
                    session.commit()
                except Exception as e:
                    print "From InstituteDBPipeline : Error while adding institute to database : ",e
                    session.rollback()
            return item

        if isinstance(item,CourseItem):
            inst = item['institute'][0].get("i")
            inst = session.query(InstitutesData).get(inst.id)
            if len(inst.courses)  == 0:
                #Add the course to Database
                course_abbr = item.extractAbbr()
                course_full_name = item.extractFullName()
                if len(course_abbr) > 1:
                    raise DropItem("Integrated Course %s" % item)
                course_abbr = course_abbr[0] if len(course_abbr) > 1 else ""
                if item.get('subcourses') is not None:
                    for s in item.get('subcourses'):
                        match = PipelineTools.courseClosestMatch(str(course_abbr),course_full_name,str(s)).get('d')
                        PipelineTools.addCourseToInstitute(inst,match,duration = DateParse(item.get("duration")).getDate() , fee = item.get("fees") )
                else:
                    match = PipelineTools.courseClosestMatch(str(course_abbr),course_full_name).get('d')
                    PipelineTools.addCourseToInstitute(inst,match ,duration = DateParse(item.get("duration")).getDate() , fee = item.get("fees"))
                return item
