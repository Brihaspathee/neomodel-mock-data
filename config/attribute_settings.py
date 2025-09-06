import importlib
import json
from pathlib import Path
from typing import Dict, List, Any
from config.attributes_mapping import AttributeMapping

ATTRIBUTES_CONFIG:Dict[str, Dict[str, AttributeMapping]] = {}

# -----------------------------------------------------------------------------------------
# Helper: import class from string
# -----------------------------------------------------------------------------------------
def import_class(full_class_path: str):
    """
    Helper function that imports a class from a full class path
    :param full_class_path:
    :return:
    """
    module_name, class_name = full_class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

# -----------------------------------------------------------------------------------------
# Load entity attributes from JSON file
# -----------------------------------------------------------------------------------------
def load_entity_attributes(entity_name: str, file_path: Path):
    with open(file_path, "r") as f:
        raw = json.load(f)
    entity_dict = {}
    for attr_id, details in raw.items():
        node_class = import_class(details["class"])
        entity_dict[attr_id] = AttributeMapping(
            name=details["name"],
            category=details["category"],
            attr_type=details["attr_type"],
            node_class=node_class,
            fields=details["fields"],
            ignore=details.get("ignore", []),
            adornments=details.get("adornments", {})
        )
    ATTRIBUTES_CONFIG[entity_name] = entity_dict

# -----------------------------------------------------------------------------------------
# Load all entities at startup
# -----------------------------------------------------------------------------------------
def load_all_attributes():
    base_dir = Path(__file__).parent / "attributes"
    for entity_dir in base_dir.iterdir():
        if entity_dir.is_dir():
            for json_file in entity_dir.glob("*.json"):
                entity_name = entity_dir.name
                load_entity_attributes(entity_name, json_file)

