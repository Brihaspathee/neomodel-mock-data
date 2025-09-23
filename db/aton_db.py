from config import settings
from neomodel import config, db
import logging

log = logging.getLogger(__name__)

def init_db():
    log.debug("Initializing DB")
    user: str = settings.NEO4J["username"]
    password: str = settings.NEO4J["password"]
    host: str = settings.NEO4J["host"]
    port: str = settings.NEO4J["port"]
    database: str = settings.NEO4J["database"]

    config.DATABASE_URL = f"bolt://{user}:{password}@{host}:{port}/{database}"

    # Test the connection immediately
    try:
        results, _ = db.cypher_query("RETURN 1 AS ok")
        if results[0][0] == 1:
            log.debug(f"✅ Connected to Neo4j database '{database}' at {host}:{port}")
    except Exception as e:
        log.debug(f"❌ Could not connect to Neo4j: {e}")
        raise