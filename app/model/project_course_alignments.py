from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectCourseAlignment(Base):
    __tablename__ = 'project_course_alignments'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, nullable=False)
    legend = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __init__(self, course_id, legend, description, id=None):
        self.course_id = course_id
        self.legend = legend
        self.description = description
        self.id = id
