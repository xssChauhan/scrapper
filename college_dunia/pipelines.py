# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, scoped_session
from models import InstitutesData , db_connect
from college_dunia.items import InstituteItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class BasePipeline():
    def __init__(self):
        engine = db_connect()
        self.Session = scoped_session(sessionmaker(bind = engine ))

class InstituteDBPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item , InstituteItem):
            session = self.Session()
            institute = InstitutesData(**item)
            try:
                session.add(institute)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item
