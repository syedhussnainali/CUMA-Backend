from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Program(Base):
    __tablename__ = 'program'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    academic_level = Column(String)
    faculty_id = Column(Integer)
    document_id = Column(String)
    latest_modified = Column(Date)
    state = Column(String)

    def __init__(self, name, academic_level, faculty_id, document_id, latest_modified, state, id = None):
        self.name = name
        self.academic_level = academic_level
        self.faculty_id = faculty_id
        self.document_id = document_id
        self.latest_modified = latest_modified
        self.id = id
        self.state = state
