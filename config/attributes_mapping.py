import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Type, Optional


@dataclass
class FieldMapper:
    mapping_type: str
    # The "code_type" represents an FMG code type if mapping_type is "code".
    # The "code_type" is optional if mapping_type is "literal".
    code_type: str
    mappings: Dict[str, str]

@dataclass
class FieldTransformer:
    transform_type: str
    # The value will be a string if the transform type is either "code" or "literal".
    # The "code" represents a FMG code type.
    # The "literal" represents a literal value.
    # The value will be FieldMapper if the transform type is "mapping".
    # The value Any is future proofing for any other pattern
    value: str | FieldMapper | Any

@dataclass
class FieldInfo:
    property: str
    type: str # "string" | "number" | "date" | "boolean" | "object" | "array" | "list" | "object"
    item_type: Optional[str] = None # Used if type == "list"
    class_path: Optional[str] = None # Optional: for nested object list

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
    fields: Dict[str, FieldInfo]
    node_class: Type
    ignore: List[str] = field(default_factory=list)
    adornments: Dict[str, Any] = field(default_factory=dict)
    conditions: Dict[str, Any] = field(default_factory=dict)
    field_transformers : Dict[str, list[FieldTransformer]] = field(default_factory=dict)



