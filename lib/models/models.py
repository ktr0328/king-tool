import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

from lib.config_loader import config as conf

engine = sqlalchemy.create_engine(
    conf.db.get('uri'),
    encoding=conf.db.get('encoding'),
    echo=conf.db.get('echo'))
Base = sqlalchemy.ext.declarative.declarative_base()


class SubjectGroup(Base):
    __tablename__ = 'subjectGroups'
    Id = Column(
        sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)
    Code = Column(String(50))
    CodeEx = Column(String(50))
    HideStd = Column(sqlalchemy.BOOLEAN)
    Name = Column(String(100))
    Order = Column(String(100))
    PictureUrl = Column(String(200))
    Type = Column(sqlalchemy.Integer)
    Year = Column(sqlalchemy.Integer)

    report = relationship('Report', backref="subjectGroups")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Report(Base):
    __tablename__ = 'reports'
    TaskID = Column(
        sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)
    DisplayDate = Column(sqlalchemy.String(50))
    GroupID = Column(
        sqlalchemy.Integer,
        ForeignKey('subjectGroups.Id', onupdate='CASCADE', ondelete='CASCADE'))
    GroupName = Column(String(50))
    IsResubmit = Column(sqlalchemy.BOOLEAN)
    PictureUrl = Column(String(200))
    Status = Column(sqlalchemy.Integer)
    SubmissionEnd = Column(String(50))
    TaskKind = Column(sqlalchemy.Integer)
    TaskType = Column(sqlalchemy.Integer)
    Title = Column(String(50))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Event(Base):
    __tablename__ = 'events'
    id = Column(
        sqlalchemy.Integer, primary_key=True, nullable=False, unique=True)
    allDay = Column(sqlalchemy.BOOLEAN)
    color = Column(String(15))
    description = Column(String(1000))
    endfortip = Column(String(50))
    groupname = Column(String(50))
    location = Column(String(50))
    senderid = Column(String(10))
    start = Column(sqlalchemy.Integer)
    end = Column(sqlalchemy.Integer)
    startfortip = Column(String(50))
    startfortip = Column(String(50))
    textColor = Column(String(20))
    title = Column(String(50))
    userid = Column(String(50))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
db = Session()
