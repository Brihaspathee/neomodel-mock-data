import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any


# -------------------------------------------------------------------------------
# Attribute Mapping Data class
# -------------------------------------------------------------------------------
@dataclass
class AttributeMapping:
    """
    Class for mapping attributes from the source data to the target data.
    """
    name: str
    category: str
    attr_type: str
    fields: Dict[str, str]
    ignore: List[str] = field(default_factory=list)
    adornments: Dict[str, Any] = field(default_factory=dict)
    class_path: str = ""
