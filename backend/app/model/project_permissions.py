from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProjectPermissions(Base):
    __tablename__ = 'project_permissions'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)
    read = Column(Boolean, nullable=False)
    read_write = Column(Boolean, nullable=False)


    def __init__(self, project_id, user_id, read, read_write, id=None):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id
        self.read = read
        self.read_write = read_write
