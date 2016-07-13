from sqlalchemy import or_,create_engine ,Enum, Column , Integer,Text , String , DateTime,ForeignKey,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Table
dbuser = "root"
dbpass = "shikhar"
dbhost = "localhost"
dbname = "edunuts_beta"

Base = declarative_base()

def db_connect():
    return create_engine("mysql+pymysql://%s:%s@%s/%s"%(dbuser,dbpass,dbhost,dbname),pool_recycle = 1800)

class Basest():

    def __init__(self,*args,**kwargs):
        self.metad = kwargs
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




institute_facilities = Table("institute_facilities",Base.metadata,
    Column("inst_id",Integer,ForeignKey("institutes.id")),
    Column("fac_id",Integer,ForeignKey("facilities.facility_id")))


class InstitutesData(Institutes):
    __tablename__ = "institutes_data"
    inst_id = Column(Integer , ForeignKey("institutes.id"),primary_key = True)
    website = Column(String)
    founded_in = Column(String)
    about = Column(Text)
    address = Column(String)
    facilities = relationship("Facilities",secondary = institute_facilities)

    @classmethod
    def getFromURL(self,url,session):
        return session.query(self).filter(self.website.like("%" + url + "%")).first()

    def setFacilities(self,session,facilities):
        for e in facilities:
            fac = session.query(Facilities).filter(Facilities.facility_name.like("%"+str(e)+"%")).first()
            if fac is not None:
                self.facilities.append(fac)

    def setCompanies(self,session,companies):
        # for e in companies:
        #     com = session.query(Companies).filter(Companies.company_name.like("%"+str(e)+"%")).first()
        #     if com is not None:
        #         instC = InstitutesCompanies()
        #         instC.company = com
        #         self.companies.append(instC)
        pass


    
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


class Facilities(Base):
    __tablename__ = "facilities"
    facility_id = Column(Integer,primary_key = True)
    facility_name = Column(String)

    @property
    def name(self):
        return self.facility_name
    


class Companies(Base):
    __tablename__ = "companies"
    company_id = Column(Integer,primary_key = True)
    company_name  = Column(String)
    verified = Enum('0','1')

    @property
    def name(self):
        return self.company_name
    
class InstituteCompanies(Base):
    __tablename__ = "institute_companies"
    inst_company_id = Column(Integer,primary_key = True)
    inst_id = Column(Integer,ForeignKey("institutes.id"))
    company_id = Column(Integer,ForeignKey("companies.company_id"))
    institute = relationship("Institutes",backref = "companies")
    company = relationship("Companies",backref = "institutes")

    @property
    def id(self):
        return self.inst_company_id
    
    def getCompanyName(self):
        return self.company.name

    def getInstituteName(self):
        return self.institute.name    