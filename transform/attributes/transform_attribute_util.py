import importlib
from datetime import datetime, date
from typing import Any, Type

from neomodel.sync_.core import NodeMeta

from config.attribute_settings import SPECIAL_ATTRIBUTES, import_class
from config.attributes_mapping import AttributeMapping, FieldInfo
from neomodel import StructuredNode
import portico_reads.service.fmg_codes.load_fmg_codes as fmg_loader

import logging

log = logging.getLogger(__name__)


def build_node_for_attribute(mapping:AttributeMapping,
                             attribute_fields: dict[str, Any]) -> StructuredNode | None:
    """
    Builds a structured node for a given attribute mapping and its corresponding fields.

    This function evaluates conditions for the provided mapping and creates a
    structured node only if all specified conditions are met. If conditions are not
    met, the function will log the event and return None. Properties of the node are
    mapped and transformed based on the given attribute mapping, ignoring fields that
    are explicitly stated to be excluded.

    :param mapping: The attribute mapping configuration defining the structured node
                    creation logic, including field mappings, ignored fields, and any
                    adornments to be applied.
    :type mapping: AttributeMapping
    :param attribute_fields: A dictionary containing fields associated with the attribute,
                             where keys are field ids and values are their respective
                             values.
    :type attribute_fields: dict[str, Any]
    :return: A StructuredNode instance created using the provided attribute mapping and
             attribute fields, or None if the conditions are not satisfied.
    :rtype: StructuredNode | None
    """
    log.debug(f"Building node for attribute {mapping.name}")
    if not evaluate_conditions(mapping, attribute_fields):
        log.debug("Conditions not met, skipping node creation")
        return None
    else:
        log.debug("Conditions met, creating node")
    props = {}
    log.debug(f"Mapping fields: {mapping.fields}")
    for field_id, field_value in attribute_fields.items():
        if field_id in mapping.ignore:
            continue
        if field_id in mapping.fields:
            field_info_dict:dict = mapping.fields[field_id]
            field_info = FieldInfo(**field_info_dict)
            # Check if the field has a transformer
            if field_id in mapping.field_transformers:
                field_value = transform_field(field_value, mapping.field_transformers[field_id])
                if isinstance(field_value, NodeMeta):
                    log.debug(f"It is node metadata")
                    mapping.node_class = field_value
                elif field_value == "":
                    continue
            # Type conversion
            field_value = _convert_field_type(field_value, field_info)
            # Assign property
            prop_name = field_info.property
            if field_info.type == "list":
                props.setdefault(prop_name, []).append(field_value)
            else:
                props[prop_name] = field_value

    props.update(mapping.adornments)
    log.debug(f"Aton Properties: {props}")
    log.debug(f"Aton Node Class: {mapping.node_class}")
    node_instance = mapping.node_class(**props)
    log.debug(f"Node instance: {node_instance}")
    return node_instance


def _convert_field_type(value: any, field_info: FieldInfo) -> Any:
    if value is None:
        return None
    if field_info.type == "date":
        # handle date conversion
        log.debug(f"Converting value {value} to date its type is {type(value)}")
        if isinstance(value, date):
            log.debug(f"it is an instance of datetime")
            # return value.isoformat()
            # try:
            #     return datetime.strptime(value, "%Y-%m-%d").date()
            # except ValueError:
            #     try:
            #         return datetime.strptime(value, "%m/%d/%Y").date()
            #     except ValueError:
            #         return value # leave it as-is if format is unknown
        return value
    if field_info.type == "int":
        return int(value)
    if field_info.type == "float":
        return float(value)
    if field_info.type == "list" and field_info.item_type == "object" and field_info.class_path:
        module_name, class_name = field_info.class_path.rsplit(".", 1)
        cls = getattr(importlib.import_module(module_name), class_name)
        return cls(**value)
    return value

def evaluate_conditions(mapping: AttributeMapping, attribute_fields: dict[str, Any]) -> bool:
    """
    Evaluates a set of conditions on provided attribute values.

    This function checks a list of conditions defined within an ``AttributeMapping``
    instance against a dictionary of attribute values. Each condition specifies a
    field, an operator, and an expected value. The function evaluates these conditions
    and determines whether they are all satisfied based on the given values.

    :param mapping: The ``AttributeMapping`` object containing the list of conditions
        to evaluate. Each condition includes a field identifier, an operator,
        and an expected value.
    :param attribute_fields: A dictionary where keys represent field IDs and the values
        are the actual attribute values to compare against the conditions.
    :return: A boolean value indicating whether all conditions are satisfied.
        Returns ``True`` if all the conditions are met, or ``False`` otherwise.
    """
    conditions = getattr(mapping, "conditions", [])
    log.debug(f"Conditions: {conditions}")
    for condition in conditions:
        operator = condition["operator"]
        field_id = condition["field_id"]
        if operator == "not null":
            if field_id not in attribute_fields:
                return False
            else:
                continue
        expected_value = condition["value"]
        actual_value = attribute_fields.get(field_id)
        log.debug(f"Actual Value: {actual_value}")
        log.debug(f"Expected Value: {expected_value}")
        log.debug(f"Operator: {operator}")
        if operator == "equals" and actual_value != expected_value:
            return False
        elif operator == "not_equals" and actual_value == expected_value:
            return False
    return True

def transform_field(data: str, transformer_list: list[Any]) -> str | Type:
    log.debug("Field Id to be transformed: " + data)
    log.debug(f"Transformers: {transformer_list}" )
    transformed_data = ""
    for transformer in transformer_list:
        log.debug(f"Transformer: {transformer}")
        split_data = ""
        transform_type = transformer["transform_type"]
        value = transformer["value"]
        if transform_type == "code":
            fmg_type = value
            log.debug(f"FMG Type:{fmg_type}")
            log.debug(f"Looking up code from FMG_CODES:{fmg_loader.FMG_CODES[fmg_type][data]}")
            split_data = fmg_loader.FMG_CODES[fmg_type][data]
        if transform_type == "literal":
            log.debug(f"Literal value:{value}")
            split_data = value
        if transform_type == "mapping":
            log.debug(f"Mapping value:{value}")
            mapping_type = value["mapping_type"]
            mappings = value["mappings"]
            if mapping_type == "literal":
                try:
                    split_data = mappings[data]
                except KeyError:
                    log.debug(f"Literal mapping not found for {data}, hence it will not be loaded")
                # split_data = mappings[data]
            if mapping_type == "code":
                fmg_type = value["code_type"]
                split_data = mappings[fmg_loader.FMG_CODES[fmg_type][data]]
            if mapping_type == "inheritance":
                log.debug(f"Inheritance mapping for the field id {data} is to be determined")
                sub_class_string = mappings[data]
                log.debug(f"Sub Class String: {sub_class_string}")
                node_class: Type = import_class(sub_class_string)
                log.debug(f"Node Class: {node_class}")
                log.debug(f"Node Class Name: {node_class.__name__}")
                log.debug(f"Node Class type: {type(node_class)}")
                log.debug(f"Node Class test: {isinstance(node_class, NodeMeta)}")
                return node_class

        transformed_data = transformed_data + split_data
    log.debug("Transformed Data: " + transformed_data)
    return transformed_data

def transform_special_attribute(attribute_id: int, *args):
    func_info = SPECIAL_ATTRIBUTES[str(attribute_id)]
    special_attribute_func = func_info["func_name"]
    func_name = _resolve(special_attribute_func)
    # ---------------------------------------------------------------------------------------------
    # create a dictionary of arguments and their values from the args list
    # kwargs = {}
    # arg_index = 0
    # for kw_argument in func_info["arguments"]:
    #     kwargs[kw_argument] = args[arg_index]
    #     arg_index += 1
    # use a dictionary comprehension to build the kwargs dictionary dynamically from two lists
    # the first list contains the argument names, the second list contains the argument values
    # long form of writing this code is above this comment
    # ---------------------------------------------------------------------------------------------
    kwargs = {k: v for k, v in zip(func_info["arguments"], args)}
    log.debug(f"Special Attribute function name: {special_attribute_func}")
    log.debug(f"Special Attribute function: {func_name}")
    log.debug(f"Special Attribute kwargs: {kwargs}")
    func_name(**kwargs)


def _resolve(func_path: str):
    """
    Resolves a fully qualified function path to the corresponding callable object.

    This function takes a string representing the fully qualified path of a
    function, loads the corresponding Python module, and retrieves the callable
    object referred to by the function path. It is commonly used for dynamic
    function resolution.

    :param func_path: The fully qualified path to a function in the format
        "module.submodule.function_name".
    :type func_path: str
    :return: The callable object corresponding to the given function path.
    :rtype: Callable
    """
    module_name, func_name = func_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)