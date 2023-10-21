from app import engine
from sqlalchemy.orm import sessionmaker

def createSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def closeSession(session):
    session.close()
