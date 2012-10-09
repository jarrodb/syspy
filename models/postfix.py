from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(), primary_key=True)
    password = Column(String())
    quota = Column(String())
    comment = Column(String())

    def __repr__(self):
        return "<User('%s')>" % (self.email)

class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    domain = Column(String(), primary_key=True)
    date = Column(DateTime())

    def __repr__(self):
        return "<Domain('%s')>" % (self.domain)

class Forwardings(Base):
    __tablename__ = 'forwardings'

    source = Column(String(), primary_key=True)
    destination = Column(String())

    def __repr__(self):
        return "<Forwarding(%s->%s)>" % (self.source, self.destination)
