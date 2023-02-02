from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from wedding.cfg import app_configuration
from wedding.extensions.store import repo
from wedding.extensions.store.utils.utils import import_submodules

engine = create_engine(app_configuration.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

import_submodules(repo)

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
