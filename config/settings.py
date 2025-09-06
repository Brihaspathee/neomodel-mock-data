import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, List, Any

from sqlalchemy.orm import relationship

from config.attributes_mapping import AttributeMapping
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

ATTRIBUTES_CONFIG:Dict[str, Dict[str, AttributeMapping]] = {}

# -----------------------------------------------------------------------------------------
# Load entity attributes from JSON file
# ---------------------------------------------------------------------------------------
def load_entity_attributes(entity_name: str, file_path: Path):
    with open(file_path, "r") as f:
        raw = json.load(f)
    entity_dict = {}
    for attr_id, details in raw.items():
        entity_dict[attr_id] = AttributeMapping(
            name=details["name"],
            category=details["category"],
            attr_type=details["attr_type"],
            class_path=details["class"],
            fields=details["fields"],
            ignore=details.get("ignore", []),
            adornments=details.get("adornments", {})
        )
    ATTRIBUTES_CONFIG[entity_name] = entity_dict

# -----------------------------------------------------------------------------------------
# Load all entities at startup
# -----------------------------------------------------------------------------------------
def load_all_attributes(base_dir: Path):
    for entity_dir in base_dir.iterdir():
        if entity_dir.is_dir():
            for json_file in entity_dir.glob("*.json"):
                entity_name = entity_dir.name
                load_entity_attributes(entity_name, json_file)

BASE_ATTRIBUTES_DIR = Path(__file__).parent / "attributes"
load_all_attributes(BASE_ATTRIBUTES_DIR)