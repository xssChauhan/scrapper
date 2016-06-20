from sqlalchemy import create_engine , Column , Integer,Text , String , DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

dbuser = "root"
dbpass = "shikhar"
dbhost = "localhost"
dbname = "edunuts_beta"

Base = declarative_base()

def db_connect():
    return create_engine("mysql+pymysql://%s:%s@%s/%s"%(dbuser,dbpass,dbhost,dbname),pool_recycle = 1800)


class Institutes(Base):
    __tablename__ = "institutes"
    id = Column(Integer , primary_key = True)
    name = Column(String)
    status = Column(String)

class InstitutesData(Institutes):
    __tablename__ = "institutes_data"
    inst_id = Column(Integer , ForeignKey("institutes.id"),primary_key = True)
    website = Column(String)
    founded_in = Column(String)
    about = Column(Text)
    address = Column(String)

class CourseNames(Base):
    __tablename__ = "course_names"
    name = Column(String)
    fullname = Column(String)

class CourseLevels(Base):
    __tablename__ = "course_levels"
    id = Column(Integer , primary_key = True)
    name = Column(String)

class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer , primary_key = True)
    course_id = Column(Integer , ForeignKey("course_names.id"))
    level_id = Column(Integer , ForeignKey("course_levels.id"))
    duration = Column(String)
