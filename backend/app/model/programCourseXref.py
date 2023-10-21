from sqlalchemy import Column, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProgramCourseXref(Base):
    __tablename__ = 'program_course_xref'

    id = Column(BigInteger, primary_key=True, default=None)
    program_id = Column(BigInteger, nullable=False)
    course_id = Column(BigInteger, nullable=False)
    core = Column(Boolean)

    def __init__(self, program_id, course_id, core = False, id=None):
        self.id = id
        self.program_id = program_id
        self.course_id = course_id
        self.core = core
