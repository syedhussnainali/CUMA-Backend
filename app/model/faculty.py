from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Faculty(Base):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    