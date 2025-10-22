import json
from pathlib import Path
from typing import Dict, Any

# -------------------------
# Global Qualification Rules mapping
# -------------------------
QUALIFICATION_RULES: Dict[str, Any] = {}


def load_qual_rules():
    global QUALIFICATION_RULES
    """Load county state mapping JSON into memory."""
    with open(QUALIFICATION_RULES_FILE, "r") as f:
        QUALIFICATION_RULES = json.load(f)


# -------------------------
# Load qualification rules at startup
# -------------------------
MAPPING_DIR = Path(__file__).parent / "mapping"
QUALIFICATION_RULES_FILE = MAPPING_DIR / "qualification_rules.json"