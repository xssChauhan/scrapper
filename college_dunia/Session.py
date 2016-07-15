from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

dbuser = "root"
dbpass = "shikhar"
dbhost = "localhost"
dbname = "edunuts_beta"



class BaseSession():
    def __init__(self):
        engine = self.db_connect()
        self.Session = scoped_session(sessionmaker(bind = engine ))

    def db_connect(self):
        return create_engine("mysql+pymysql://%s:%s@%s/%s"%(dbuser,dbpass,dbhost,dbname),pool_recycle = 1800)

    def makeSession(self):
        return self.Session()

session = BaseSession().makeSession()
