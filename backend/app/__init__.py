from flask import Flask
from flask_cors import CORS
import psycopg2
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, supports_credentials=True)
#app.config['SESSION_TYPE'] = 'filesystem'  # Can be any session type you prefer
#app.config['SESSION_COOKIE_SECURE'] = True  # Ensure secure session cookie for production
#app.config['SESSION_COOKIE_HTTPONLY'] = True  # Restrict session cookie access to HTTP-only
#app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Apply strict same-site policy
#Session(app)


# DB connection
conn = psycopg2.connect(
    host="localhost",
    database="cuma",
    user="postgres",
    password=os.environ.get("PG_PASS"),
)
engine = create_engine('postgresql://postgres:harsha@localhost:5432/cuma')

# include for routing should always at the end of file
from app import routes
