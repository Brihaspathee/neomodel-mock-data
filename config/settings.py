import json
import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy.orm import relationship

from config.secrets_api import SecretsAPI
import logging
from config import aton_logging
# from transform.attribute_transformer import AttributeStructure

aton_logging.setup_logging()
log = logging.getLogger(__name__)



def fetch_secrets():
    log.info("Fetching Secrets using log")
    db_secrets = SecretsAPI(["ss.neo4j.url",
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
    "username": secrets["ss.neo4j.username"],
    "port": secrets["ss.neo4j.port"],
    "host": secrets["ss.neo4j.host"],
    "password": secrets["ss.neo4j.password"],
    "database": secrets["ss.neo4j.database"],
}

# Path to the attributes.json file that has all the attributes
CONFIG_PATH = Path(__file__).with_name("attributes.json")

# The code below is reading the attributes.json file and
# transforms it into a flattened structure

# Load the grouped config
with open(CONFIG_PATH, "r") as f:
    GROUPED_CONFIG = json.load(f)
# GROUPED CONFIG contains the attributes json file grouped by entity type

# Build flat config for fast lookups
FLAT_CONFIG = {}
for entity_type, attributes in GROUPED_CONFIG.items():
    # - Iterates through each key-value pair in `GROUPED_CONFIG`
    # entity_type will be the key, attributes will be the value
    # entity_type = "provider"
    # attributes = {"101": {"category": "identifier", "name": "PROV_NPI"}
    for attribute_id, details in attributes.items():
        # - Iterates through each key-value pair in `attributes`
        # attribute_id will be the key, details will be the value
        # attribute_id = "101"
        # details = {"category": "identifier", "name": "PROV_NPI"}

        # Build the flat config
        # attribute_id becomes the key in flat config
        FLAT_CONFIG[attribute_id] = {
            # the value is the dictionary with keys, "entity_type", "category", "name"
            "entity_type": entity_type,
            **details, # this is dictionary unpacking
            # **details is equivalent to writing the below code
            # "category": details["category"], "name": details["name"], "field_mappings": details["field_mappings"]
        }

# FLAT_CONFIG = {
#     "101": {
#         "entity_type": "provider",
#         "category": "identifier",
#         "name": "PROV_NPI",
#         "field_mappings": {
#             "1001": "PROV_NPI",
#             "1002": "PROV_NPI_START_DATE"
#         }
#     }
# }

# ATTRIBUTE_STRUCTURES: dict[str, AttributeStructure] = {
#     attr_id: AttributeStructure(
#         entity_type=cfg['entity_type'],
#         category=cfg['category'],
#         labels=cfg.get('labels'),
#         issuer=cfg.get('issuer'),
#         attr_type=cfg.get('attr_type'),
#         relationship=cfg.get('relationship'),
#         name=cfg.get('name'),
#         field_mappings=cfg.get('field_mappings'),
#         conditions=cfg.get('conditions')
#     )
#     for attr_id, cfg in FLAT_CONFIG.items()
# }