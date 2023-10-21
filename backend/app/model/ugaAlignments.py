from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UgaAlignments(Base):
    __tablename__ = 'uga_alignments'
    
    id = Column(Integer, primary_key=True, nullable=False)
    legend = Column(String)
    description = Column(String)
    
    def __init__(self, legend, description, id = None):
        self.id = id
        self.legend = legend
        self.description = description
