import click
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(dotenv_path='./conf/.env.local')

engine = create_engine(os.getenv('DATABASE_URI'))
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import api.models
    Base.metadata.create_all(bind=engine)

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialized')

def close_db(e=None):
    db_session.remove()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
