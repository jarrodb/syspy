from sqlalchemy import Column, Integer, String, DateTime, Boolean
from base import Base

class User(Base):
    __tablename__ = 'users'

    email = Column(String(), primary_key=True)
    password = Column(String())
    quota = Column(String())

    def __repr__(self):
        return "<User('%s')>" % (self.email)

class Domain(Base):
    __tablename__ = 'domains'

    domain = Column(String(), primary_key=True)

    def __repr__(self):
        return "<Domain('%s')>" % (self.domain)

class Forwardings(Base):
    __tablename__ = 'forwardings'

    source = Column(String(), primary_key=True)
    destination = Column(String())

    def __repr__(self):
        return "<Forwarding(%s->%s)>" % (self.source, self.destination)
