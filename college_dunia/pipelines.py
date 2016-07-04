# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, scoped_session
from models import InstitutesData , db_connect , Institutes
from college_dunia.items import InstituteItem
from fuzzywuzzy.fuzz import token_sort_ratio as tsor , partial_ratio as pr
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def closestMatch(s,session):
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


class BasePipeline():
    def __init__(self):
        engine = db_connect()
        self.Session = scoped_session(sessionmaker(bind = engine ))

    def makeSession(self):
        return self.Session()

class InstituteDBPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item , InstituteItem):
            session = self.Session()
            institute = InstitutesData(**item)
            match =  closestMatch(item.get('name') , session )
            if match.get('s') > 50 and match.get('d') is not None:
                print "Ignoring " + item.get('name') + " as a match was found in " + match.get('d').name
                
            else:
                print("Adding To Database" + item.get('name'))
                try:
                    session.add(institute)
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()

            return item

#Process course items here
class InstituteCourseDBPipeline(BasePipeline):
    def process_item(self,item,spider):
        print "Calling IC pipeline"
        if isinstance(item,CourseItem):
            print item
            
