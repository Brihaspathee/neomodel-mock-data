from neo4j import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import settings
import logging

log = logging.getLogger(__name__)

class PorticoDB:

    def __init__(self):
        self.SessionLocal: scoped_session[Session] | None = None
        self.engine = None
        self.db_url = None

    def connect(self):
        # define_env()
        # secrets = fetch_secrets()
        # print(secrets)
        # self.db_url = secrets["ss.portico.url"]
        self.db_url = settings.POSTGRES["db_url"]
        log.debug(self.db_url)
        if not self.db_url:
            raise ValueError("Portico DB URL not defined")

        self.engine = create_engine(self.db_url)
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        return self.SessionLocal()

    def close(self):
        self.SessionLocal.remove()
        self.engine.dispose()