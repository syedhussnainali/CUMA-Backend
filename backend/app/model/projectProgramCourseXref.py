from sqlalchemy import Column, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectProgramCourseXref(Base):
    __tablename__ = 'project_program_course_xref'

    id = Column(BigInteger, primary_key=True)
    project_id = Column(BigInteger, nullable=False)
    program_id = Column(BigInteger, nullable=False)
    course_id = Column(BigInteger, nullable=False)
    core = Column(Boolean)

    def __init__(self, project_id, program_id, course_id, id = None, core = None):
        self.id = id
        self.project_id = project_id
        self.program_id = program_id
        self.course_id = course_id
        self.core = core
