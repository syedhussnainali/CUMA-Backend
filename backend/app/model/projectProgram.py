from sqlalchemy import Column, BigInteger, Text, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectProgram(Base):
    __tablename__ = 'project_program'

    id = Column(BigInteger, primary_key=True, default=None)
    project_id = Column(BigInteger, nullable=False)
    name = Column(Text, nullable=False)
    academic_level = Column(Text)
    faculty_id = Column(BigInteger, nullable=False)
    document_id = Column(Text)
    latest_modified = Column(Date)
    revision_start_date = Column(Date)
    state = Column(Text)
    parent_program_id = Column(BigInteger)

    def __init__(self, project_id, name, faculty_id, academic_level=None, document_id=None,
                 latest_modified=None, revision_start_date=None, state=None, parent_program_id=None, id=None):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.academic_level = academic_level
        self.faculty_id = faculty_id
        self.document_id = document_id
        self.latest_modified = latest_modified
        self.revision_start_date = revision_start_date
        self.state = state
        self.parent_program_id = parent_program_id
