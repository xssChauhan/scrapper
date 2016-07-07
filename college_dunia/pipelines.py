# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import or_
from models import InstitutesData , db_connect , Institutes,Courses,CourseNames, Subcourses, InstituteCourses,CrawlChange
from college_dunia.items import InstituteItem, CourseItem
from fuzzywuzzy.fuzz import token_sort_ratio as tsor , partial_ratio as pr
import re
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
class BasePipeline():
    def __init__(self):
        engine = db_connect()
        self.Session = scoped_session(sessionmaker(bind = engine ))

    def makeSession(self):
        return self.Session()

session = BasePipeline().makeSession()

def closestMatch(s):
    match = {
        "s" : 0,
    }
    toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]


    for e in xrange(len(toMatch)//2 - 1,len(toMatch)):
        i = Institutes.likeAll(toMatch[e],session)
        for t in i:
            score = tsor(s,t.name)
            if score > match['s']:
                match['s'] = score
                match['d'] = t
    return match

def courseClosestMatch(abbr,fullname,subcourse = ""):
    match = {
        "s" : 0, 
    }
    s = abbr + " " + fullname
    toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]
    for e in xrange(len(toMatch)//2 - 1,len(toMatch)):
        i = session.query(Courses).join(Courses.course).join(Courses.subcourse).filter(or_(CourseNames.name.like("%"+abbr+"%"),CourseNames.fullname.like("%"+fullname+"%"),Subcourses.name.like("%"+ subcourse +"%"))).all()
        for t in i:
            score = tsor(abbr,t.getName) + tsor(fullname,t.getFullName) + tsor(subcourse,t.getSubcourse)
            if score > match['s']:
                match['s'] = score
                match['d'] = t
    return match


def addCourseToInstitute(inst,course, **kwargs):
    try:
        ic = InstituteCourses(**kwargs)
        ic.course = course
        inst.courses.append(ic)
        
        session.commit()
        session.add(CrawlChange(table_name = ic.__tablename__ , modification = "new" , entity = ic.id))
        session.commit()
    except Exception as e:
        print "Error while adding course to Institute" ,e
        session.rollback()
    else:
        print course.getName + " " + course.getFullName + " " + course.getSubcourse + " " + inst.name
    return 1



class InstituteDBPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item , InstituteItem):
            institute = InstitutesData(**item)
            match =  closestMatch(item.get('name') )
            if match.get('s') > 50 and match.get('d') is not None:
                #print "Ignoring " + item.get('name') + " as a match was found in " + match.get('d').name
                pass
            else:
                print("Adding To Database" + item.get('name'))
                try:
                    session.add(institute)
                    session.commit()
                    session.add(CrawlChange(table_name = institute.__tablename__,modification = "new",entity = institute.id))
                    session.commit()
                except Exception as e:
                    print "Error while adding institute to database ",e
                    session.rollback()
                    raise
                finally:
                    session.close()

            return item

        if isinstance(item,CourseItem):
            inst = item['institute'][0].get("i")
            if len(inst.courses)  == 0:
                #Add the course to Database
                course_abbr = item.extractAbbr()
                course_full_name = item.extractFullName()
                if len(course_abbr) > 1:
                    raise DropItem("Integrated Course %s" % item)
                course_abbr = course_abbr[0] if len(course_abbr) > 1 else ""
                if item.get('subcourses') is not None:
                    for s in item.get('subcourses'):
                        match = courseClosestMatch(str(course_abbr),course_full_name,str(s)).get('d')
                        addCourseToInstitute(inst,match,duration = item.get("duration") , fee = item.get("fees") )
                else:
                    match = courseClosestMatch(str(course_abbr),course_full_name).get('d')
                    addCourseToInstitute(inst,match,duration = item.get("duration") , fee = item.get("fees"))
                return item


