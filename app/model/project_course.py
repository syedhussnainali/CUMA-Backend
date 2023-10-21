from sqlalchemy import Column, BigInteger, Text, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectCourse(Base):
    __tablename__ = 'project_course'

    id = Column(BigInteger, primary_key=True)
    project_id = Column(BigInteger, nullable=False)
    course_code = Column(Text, nullable=False)
    also_known_as = Column(Text)
    formerly_known_as = Column(Text)
    name = Column(Text, nullable=False)
    document_id = Column(Text)
    revision_start_date = Column(Date, nullable=False)
    latest_modified = Column(Date)
    state = Column(Text)
    parent_course_id = Column(BigInteger)

    def __init__(self, project_id, course_code, also_known_as, formerly_known_as, name, document_id, revision_start_date, latest_modified, state, id=None, parent_course_id = None):
        self.project_id = project_id
        self.course_code = course_code
        self.also_known_as = also_known_as
        self.formerly_known_as = formerly_known_as
        self.name = name
        self.document_id = document_id
        self.revision_start_date = revision_start_date
        self.latest_modified = latest_modified
        self.state = state
        self.id = id
        self.parent_course_id = parent_course_id
