import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./conf/.env.local')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI')