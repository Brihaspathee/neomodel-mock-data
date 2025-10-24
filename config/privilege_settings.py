import json
from pathlib import Path
from typing import Dict

# -------------------------
# Global Privilege Type Mapping
# -------------------------
PRIVILEGE_TYPE_MAPPING: Dict[str, str] = {}


def load_hosp_priv_mapping():
    """Load hospital privilege type mapping JSON into memory."""
    with open(HOSP_PRIV_MAPPING_FILE, "r") as f:
        raw = json.load(f)

    global PRIVILEGE_TYPE_MAPPING
    PRIVILEGE_TYPE_MAPPING = raw
    # ADDRESS_USE_MAPPING = raw.get("address_types", {})


# -------------------------
# Load mapping at startup
# -------------------------
MAPPING_DIR = Path(__file__).parent / "mapping"
HOSP_PRIV_MAPPING_FILE = MAPPING_DIR / "hosp_priv_mapping.json"