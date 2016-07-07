from sqlalchemy import or_,create_engine , Column , Integer,Text , String , DateTime,ForeignKey,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

dbuser = "root"
dbpass = "shikhar"
dbhost = "localhost"
dbname = "edunuts_beta"

Base = declarative_base()

def db_connect():
    return create_engine("mysql+pymysql://%s:%s@%s/%s"%(dbuser,dbpass,dbhost,dbname),pool_recycle = 1800)

class Basest():
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id =  Column(Integer, primary_key=True)

    @classmethod
    def likeAll(self,attr,string,session):
        return session.query(self).filter(getattr(self,attr).like("%" + string + "%")).all()

class Institutes(Base,Basest):
    __tablename__ = "institutes"
    id = Column(Integer , primary_key = True)
    name = Column(String)
    status = Column(String)
    courses = relationship("InstituteCourses")

    @classmethod
    def likeAll(self,string,session):
        return session.query(self).filter(self.name.like("%" + string + "%")).all()






class InstitutesData(Institutes):
    __tablename__ = "institutes_data"
    inst_id = Column(Integer , ForeignKey("institutes.id"),primary_key = True)
    website = Column(String)
    founded_in = Column(String)
    about = Column(Text)
    address = Column(String)

    @classmethod
    def getFromURL(self,url,session):
        return session.query(self).filter(self.website.like("%" + url + "%")).first()


    
class Subcourses(Base,Basest):
    __tablename__ = "subcourses"
    id = Column(Integer,primary_key = True)
    name = Column(String)

class CourseNames(Base,Basest):
    __tablename__ = "course_names"
    id = Column(Integer , primary_key = True)
    name = Column(String)
    fullname = Column(String)

class CourseLevels(Base,Basest):
    __tablename__ = "course_levels"
    id = Column(Integer , primary_key = True)
    name = Column(String)

class Courses(Base,Basest):
    __tablename__ = "courses"
    id = Column(Integer , primary_key = True)
    course_id = Column(Integer , ForeignKey("course_names.id"))
    level_id = Column(Integer , ForeignKey("course_levels.id")) 
    subcourse_id = Column(Integer,ForeignKey("subcourses.id"))
    duration = Column(String)
    course = relationship("CourseNames")
    subcourse = relationship("Subcourses")
    

    @property
    def getName(self):
        return self.course.name

    @property
    def getFullName(self):
        return self.course.fullname
    @property
    def getSubcourse(self):
        return self.subcourse.name
    



 
    




class InstituteCourses(Base, Basest):
    __tablename__ = "institute_courses"
    id = Column(Integer,primary_key = True)
    inst_id = Column(Integer,ForeignKey("institutes.id"))
    course_id = Column(Integer,ForeignKey("courses.id"))
    seats = Column(Integer)
    fee = Column(Integer)
    duration = Column(String)
    course = relationship("Courses",backref="institutes")
    institute = relationship("Institutes")
    
    @classmethod
    def courseInInstitute(self,fullname,abbr,session):
        results = session.query(self,Courses).join(self.institute).join(self.course).join(Courses.course).filter(and_(CourseNames.name.like("%"+abbr+"%"),CourseNames.fullname.like("%"+ fullname +"%"))).all()
        return iter([ e[1] for e in results ])

class CrawlChange(Base):
    __tablename__ = "crawl_changed"
    id = Column(Integer,primary_key = True)
    table_name = Column(String)
    entity = Column(String)
    modification = Column(String)