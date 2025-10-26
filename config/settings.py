
import os
from dotenv import load_dotenv
from pathlib import Path
from config.attribute_settings import load_all_attributes
from config.contact_settings import load_contact_mapping, CONTACT_MAPPING_FILE
from config.county_settings import load_county_mapping


from sqlalchemy.orm import relationship

from config.map_reader.cred_type_geo_map import load_cred_geo_mapping
from config.privilege_settings import load_hosp_priv_mapping
from config.qualification_rules_settings import load_qual_rules
from config.secrets_api import SecretsAPI
import logging
from config import aton_logging
# from transform.attribute_transformer import AttributeStructure

aton_logging.setup_logging()
log = logging.getLogger(__name__)



def fetch_secrets():
    log.debug("Fetching Secrets using log")
    db_secrets = SecretsAPI(["ss.neo4j.url",
                             "ss.neo4j.protocol",
                             "ss.neo4j.username",
                             "ss.neo4j.password",
                             "ss.neo4j.database",
                             "ss.neo4j.port",
                             "ss.neo4j.host",
                             "ss.portico.url"])
    secrets = db_secrets.get_secrets()
    return secrets

# Determine the environment
APP_ENV = os.getenv("APP_ENV", "local")

# build the path the correct .env file
ENV_DIR = Path(__file__).resolve().parent.parent / "env"
env_file = ENV_DIR / f".env.secrets.{APP_ENV}"

# Load the environment variables
load_dotenv(dotenv_path=env_file)

# Get Secrets
secrets: dict[str, str] = fetch_secrets()

# Store Environment
ENVIRONMENT = APP_ENV

# POSTGRES SQL
POSTGRES = {
    # "user": secrets["ss.neo4j.username"],
    # "password": secrets["ss.neo4j.password"],
    # "database": secrets["ss.neo4j.database"],
    # "host": secrets["ss.neo4j.url"],
    # "port": secrets["ss.neo4j.port"],
    "db_url": secrets["ss.portico.url"]
}

# NEO4J
NEO4J = {
    "url": secrets["ss.neo4j.url"],
    "protocol": secrets["ss.neo4j.protocol"],
    "username": secrets["ss.neo4j.username"],
    "port": secrets["ss.neo4j.port"],
    "host": secrets["ss.neo4j.host"],
    "password": secrets["ss.neo4j.password"],
    "database": secrets["ss.neo4j.database"],
}


load_all_attributes()
load_contact_mapping()
load_county_mapping()
load_hosp_priv_mapping()
load_qual_rules()
load_cred_geo_mapping()
