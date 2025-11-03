import importlib
import json
from pathlib import Path
from typing import Dict, List, Any, Type
from config.attributes_mapping import AttributeMapping
import logging

log = logging.getLogger(__name__)

ATTRIBUTES_CONFIG:Dict[str, Dict[str, AttributeMapping]] = {}
SPECIAL_ATTRIBUTES:Dict[str, Dict[str, Any]] = {
    "100114":{
        "func_name": "transform.attributes.provider.special_prov_attributes.transform_hat_code_attr",
        "arguments": ["prov_attrib", "organization"]
    },
    "100087":{
        "func_name": "transform.attributes.provider.location.special_prov_loc_attributes.transform_panel_attr",
        "arguments": ["prov_loc_attrib", "role_instance", "prov_tin_loc"]
    }
}

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
        node_class: Type = import_class(details["class"])
        log.debug(f"********* Inside load_entity_attributes: **********")
        log.debug(f"Node class: {node_class}")
        log.debug(f"Node class name: {node_class.__name__}")
        log.debug(f"Node class type: {type(node_class)}")
        entity_dict[attr_id] = AttributeMapping(
            name=details["name"],
            category=details["category"],
            attr_type=details["attr_type"],
            node_class=node_class,
            fields=details["fields"],
            ignore=details.get("ignore", []),
            adornments=details.get("adornments", {}),
            conditions=details.get("conditions", {}),
            field_transformers=details.get("field_transformers", {})
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

