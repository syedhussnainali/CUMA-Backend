from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectProgramAlignment(Base):
    __tablename__ = 'project_program_alignments'

    id = Column(BigInteger, primary_key=True, default=None)
    program_id = Column(BigInteger, nullable=False)
    legend = Column(Text)
    description = Column(Text)

    def __init__(self, program_id, legend=None, description=None, id=None):
        self.id = id
        self.program_id = program_id
        self.legend = legend
        self.description = description
