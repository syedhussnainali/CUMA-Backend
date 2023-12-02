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

conn = conn = psycopg2.connect('postgresql://ealehddbpmkhay:2954cd87066a4ce0990c0c5b6372fcf4dc5a52f82bcee95d601121f3e2e7dd35@ec2-44-208-206-97.compute-1.amazonaws.com:5432/d9d8b0htabq5eb')

engine = create_engine('postgresql://ealehddbpmkhay:2954cd87066a4ce0990c0c5b6372fcf4dc5a52f82bcee95d601121f3e2e7dd35@ec2-44-208-206-97.compute-1.amazonaws.com:5432/d9d8b0htabq5eb')

@app.route('/')
def testmain():
    return 'testing'

# postgres://keshavsharma:8ouqic74GL1gRV6HFYzkfiyIgiVNdN8A@dpg-ckq1iehrfc9c73egiev0-a.oregon-postgres.render.com/cuma

 

# include for routing should always at the end of file

from app import routes