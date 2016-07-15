import inspect,re
from college_dunia.models import *
from fuzzywuzzy.fuzz import token_sort_ratio as tsor , partial_ratio as pr
from college_dunia.Session import session
class PipelineTools(object):

    @classmethod
    def closestMatch(self,s):
        match = {
            "s" : 0,
        }
        toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]
        for e in xrange(len(toMatch)//2 - 1,len(toMatch)):
            i = InstitutesData.likeAll(toMatch[e])
            for t in i:
                score = tsor(s,t.name)
                if score > match['s']:
                    match['s'] = score
                    match['d'] = t
        return match

    @classmethod
    def cityClosestMatch(self,s):
        match = {
            "s" : 0
        }
        toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]
        for e in xrange(len(toMatch)//2 -1, len(toMatch)):
            c = Cities.likeAll(toMatch[e])
            for t in c:
                score = tsor(s,t.name)
                if score > match.get('s'):
                    match['s'] = score
                    match['d'] = t
        return match.get('d')
    @classmethod
    def courseClosestMatch(self,abbr,fullname,subcourse = ""):
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
        return match['d']

    @classmethod
    def addCourseToInstitute(self,inst,course, **kwargs):
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

    @classmethod
    def getPincode(self,string):
        pattern = "\d{6}"
        return re.findall(pattern,string)[0]

    @classmethod
    def getLat(self,string):
        pattern = "var\s+latd\s+=\s+([\d.]+)"
        return re.findall(pattern,string)[0]

    @classmethod
    def getLang(self,string):
        pattern = "var\s+lngd\s+=\s+([\d.]+)"
        return re.findall(pattern,string)[0]

    @classmethod
    def getCity(self,string):
        return string.split(",")[0]

    @classmethod
    def getFoundedIn(self,string):
        pattern = "(\d+)"
        return re.findall(pattern,string)[0]

    @classmethod
    def getCity(self,string):
        pattern = "(\w+)"
        return re.findall(pattern,string)[0]

    @classmethod
    def makeInstituteObject(self,item , i = None):
        toAvoid = {"metadata" : None ,"facilities" : None,"companies" : None,"city" : self.cityClosestMatch ,"latitude" : self.getLat,"longitude" : self.getLang,"founded_in" : self.getFoundedIn}
        try:
            i = InstitutesData() if i is None else i
            for e in [x for x in dir(i) if not x.startswith("__") and not x.startswith("_") and x not in toAvoid and not inspect.ismethod(getattr(i,x))]:
                if item.get(e) is not None:
                    print e," ",item.get(e),type(item.get(e))
                    setattr(i,e,item.get(e))
            for n,e in toAvoid.items():
                if e is not None:
                    print n,e
                    setattr(i,n,e(item.get(n)))
            i.pincode = self.getPincode(item.get("address"))
            i.state = self.getCity(item.get("address"))
            return i
        except Exception as t:
            print "Error while making object ",t," ",e
