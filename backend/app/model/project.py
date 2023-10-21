from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    # here owner is text field intented to store the email address of the user submitted the request
    #   have used email insted of refering the usertable (user id) as FK, i dont know how the Uwindsor user database looks like 
    #   later change simply change here
    default_read = Column(Boolean, nullable=False, default=True)
    default_read_write = Column(Boolean, nullable=False, default=False)

    def __init__(self, name, owner, default_read=True, default_read_write=False, id=None):
        self.id = id
        self.name = name
        self.owner = owner
        self.default_read = default_read
        self.default_read_write = default_read_write
