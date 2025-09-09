import json
from pathlib import Path
from typing import Dict

# -------------------------
# Global Contact/Address Type Mapping
# -------------------------
CONTACT_USE_MAPPING: Dict[str, str] = {}
ADDRESS_USE_MAPPING: Dict[str, str] = {}


def load_contact_mapping():
    """Load contact/address type mapping JSON into memory."""
    with open(CONTACT_MAPPING_FILE, "r") as f:
        raw = json.load(f)

    global CONTACT_USE_MAPPING, ADDRESS_USE_MAPPING
    CONTACT_USE_MAPPING = raw.get("contact_types", {})
    ADDRESS_USE_MAPPING = raw.get("address_types", {})


# -------------------------
# Load mapping at startup
# -------------------------
MAPPING_DIR = Path(__file__).parent / "mapping"
CONTACT_MAPPING_FILE = MAPPING_DIR / "contact_use_mapping.json"