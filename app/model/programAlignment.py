from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProgramAlignment(Base):
    __tablename__ = 'program_alignments'

    id = Column(BigInteger, primary_key=True, default=None)
    program_id = Column(BigInteger, nullable=False)
    legend = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    def __init__(self, program_id, legend, description, id=None):
        self.id = id
        self.program_id = program_id
        self.legend = legend
        self.description = description
