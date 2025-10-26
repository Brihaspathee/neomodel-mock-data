from typing import Any

import pandas as pd
from pathlib import Path
import logging

log = logging.getLogger(__name__)

CRED_TYPE_GEO_MAPPING: dict[str, Any] = {}


def load_cred_geo_mapping():
    global CRED_TYPE_GEO_MAPPING
    """Load cred geo mapping CSV into memory."""
    df = pd.read_csv(CRED_GEO_MAPPING_FILE)
    df = df.rename(columns={
        "Geography Description": "geography_description",
        "Geography Type": "geography_type",
        "Description": "description",
    })
    df["FIPS"] = df["FIPS"].apply(
        lambda x: f"{int(float(x)):02}" if pd.notna(x) and str(x).strip() != "" else ""
    )
    CRED_TYPE_GEO_MAPPING = df.set_index(df.columns[0]).to_dict(orient="index")


# -------------------------
# Load mapping at startup
# -------------------------
MAPPING_DIR = Path(__file__).parent / "../mapping"
CRED_GEO_MAPPING_FILE = MAPPING_DIR / "cred_type_geo_mapping.csv"