from flask import Flask

from flask_cors import CORS

import psycopg2

import os

from sqlalchemy import create_engine

from datetime import timedelta

 

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

CORS(app, supports_credentials=True)

app.config['SESSION_TYPE'] = 'filesystem'  # Can be any session type you prefer

app.config['SESSION_COOKIE_SECURE'] = True  # Ensure secure session cookie for production

#app.config['SESSION_COOKIE_HTTPONLY'] = True  # Restrict session cookie access to HTTP-only

app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Apply strict same-site policy



 

 

# DB connection

conn = conn = psycopg2.connect(os.environ.get('DB_CONNECTION_STRING'))

engine = create_engine(os.environ.get('DB_CONNECTION_STRING'))

@app.route('/')
def testmain():
    return 'testing'

# postgres://keshavsharma:8ouqic74GL1gRV6HFYzkfiyIgiVNdN8A@dpg-ckq1iehrfc9c73egiev0-a.oregon-postgres.render.com/cuma

 

# include for routing should always at the end of file

from app import routes
