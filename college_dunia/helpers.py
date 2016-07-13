import datetime
import re
from fuzzywuzzy.fuzz import token_sort_ratio as tsor , partial_ratio as pr
def closestMatch(s , obj , session , attr = "name"):
    match = {
        "s" : 0,
        "p" : 0
    }
    toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]


    for e in xrange(len(toMatch)//2 - 1,len(toMatch)):
        i = obj.likeAll(toMatch[e],attr,session)
        for t in i:
            if not isinstance(t,NoneType):
                score = (tsor(s,t.name),pr(s,t.name))
                if score > (match['s'],match['p']):
                    match['s'] , match['p'] = score
                    match['d'] = t
    return match



def newResponse(response , body):
    r = response.copy()
    return r.replace(body = body)

def getYears(text):
    return re.findall("\d",text[0])[0]


class DateParse():

    def __init__(self , year , month = 1, day= 1, hours =  0, minutes = 0 , seconds = 0):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hours)
        self.minute = int(minutes)
        self.second = int(seconds)
        self._date = datetime.datetime(year = self.year , month = self.month , day = self.day )
        self.date = str(self._date)

    @property
    def dateRepr(self):
        return str(self._date)

    def replaceDays(self):
        pattern = "-\d{2} "
        self.date = re.sub(pattern,"-00 ",self.date)
        return self

    def replaceMonths(self):
        pattern = "-\d{2}-"
        self.date = re.sub(pattern,"-00-",self.date)
        return self

    def getDate(self):
        return self.replaceDays().replaceMonths().date
