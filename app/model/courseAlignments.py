from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CourseAlignment(Base):
    __tablename__ = 'course_alignments'

    id = Column(BigInteger, primary_key=True)
    course_id = Column(BigInteger, nullable=False)
    legend = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, course_id, legend, description, id = None):
        self.id = id
        self.course_id = course_id
        self.legend = legend
        self.description = description
