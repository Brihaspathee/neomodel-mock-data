import json
from pathlib import Path
from typing import Dict, Any

# -------------------------
# Global County/State mapping
# -------------------------
COUNTY_STATE_MAPPING: Dict[str, Any] = {}


def load_county_mapping():
    global COUNTY_STATE_MAPPING
    """Load county state mapping JSON into memory."""
    with open(COUNTY_STATE_MAPPING_FILE, "r") as f:
        COUNTY_STATE_MAPPING = json.load(f)


# -------------------------
# Load mapping at startup
# -------------------------
MAPPING_DIR = Path(__file__).parent / "mapping"
COUNTY_STATE_MAPPING_FILE = MAPPING_DIR / "county_state_mapping.json"