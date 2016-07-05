from sqlalchemy import create_engine , Column , Integer,Text , String , DateTime,ForeignKey
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

    @property
    def foo(self):
        return self._foo






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
    duration = Column(String)
    course = relationship("CourseNames")

    @property
    def getName(self):
        return self.course.name

    @property
    def getFullName(self):
        return self.course.fullname




class InstituteCourses(Base, Basest):
    __tablename__ = "institute_courses"
    id = Column(Integer,primary_key = True)
    inst_id = Column(Integer,ForeignKey("institutes.id"))
    course_id = Column(Integer,ForeignKey("courses.id"))
    seats = Column(Integer)
    course = relationship("Courses")
    institute = relationship("Institutes")
