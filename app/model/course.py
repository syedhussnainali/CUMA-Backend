from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    course_code = Column(String, nullable=False)
    also_known_as = Column(String)
    formerly_known_as = Column(String)
    name = Column(String, nullable=False)
    document_id = Column(String)
    latest_modified = Column(Date)
    state = Column(String)

    def __init__(self, course_code, also_known_as, formerly_known_as, name, document_id, latest_modified,state, id=None):
        self.course_code = course_code
        self.also_known_as = also_known_as
        self.formerly_known_as = formerly_known_as
        self.name = name
        self.document_id = document_id
        self.latest_modified = latest_modified
        self.id =id
        self.state = state