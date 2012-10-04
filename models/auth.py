from sqlalchemy import Column, Integer, String, DateTime, Boolean
from base import Base

class Auth(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True)
    token = Column(String())
    secret = Column(String())
    access = Column(Integer)

    def __repr__(self):
        return "<Auth('%d')>" % (self.access)

