from sqlalchemy import or_,create_engine ,Enum, Column , Integer,Text , String , DateTime,ForeignKey,and_ , Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from college_dunia.Session import session


Base = declarative_base()


class Basest():

    def __init__(self,*args,**kwargs):
        self.metad = kwargs
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id =  Column(Integer, primary_key=True)

    @classmethod
    def likeAll(self,attr,string):
        return session.query(self).filter(getattr(self,attr).like("%" + string + "%")).all()



class Institutes(Base,Basest):
    __tablename__ = "institutes"
    id = Column(Integer , primary_key = True)
    name = Column(String)
    status = Column(String)
    courses = relationship("InstituteCourses")
    city_id = Column(String,ForeignKey("cities.city_id"))
    city = relationship("Cities",backref = "institutes")

    @classmethod
    def likeAll(self,string):
        return session.query(self).filter(self.name.like("%" + str(string) + "%")).all()




institute_facilities = Table("institute_facilities",Base.metadata,
    Column("inst_id",Integer,ForeignKey("institutes.id")),
    Column("fac_id",Integer,ForeignKey("facilities.facility_id")))

institute_companies = Table("institute_companies",Base.metadata,
    Column("inst_id",Integer,ForeignKey("institutes.id")),
    Column("company_id",Integer,ForeignKey("companies.company_id")))

class InstitutesData(Institutes):
    __tablename__ = "institutes_data"
    inst_id = Column(Integer , ForeignKey("institutes.id"),primary_key = True)
    website = Column(String)
    founded_in = Column(String)
    about = Column(Text)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    page_url = Column(String)
    facilities = relationship("Facilities",secondary = institute_facilities,backref="institutes")
    companies = relationship("Companies",secondary = institute_companies,backref="institutes")

    @classmethod
    def getFromURL(self,url):
        return session.query(self).filter(self.website.like("%" + url + "%")).first()

    def setFacilities(self,facilities = []):
        print "Adding Facilities"
        for e in facilities:
            fac = session.query(Facilities).filter(Facilities.facility_name.like("%"+str(e)+"%")).first()
            if fac is not None and fac not in self.facilities:
                self.facilities.append(fac)
        return self

    def setCompanies(self,companies = []):
        print "Adding Companies"
        for e in companies:
            com = session.query(Companies).filter(Companies.company_name.like("%"+str(e)+"%")).first()
            if com is not None and com not in self.companies:
                self.companies.append(com)
        return self



class Cities(Base):
    __tablename__ = "cities"
    city_id = Column(Integer,primary_key = True)
    city_name = Column(String)

    @property
    def name(self):
        return self.city_name


    @classmethod
    def likeAll(self,string):
        return session.query(self).filter(self.city_name.like("%"+ string+"%")).all()

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
    def courseInInstitute(self,fullname,abbr):
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
