from typing import Any

from neomodel import StructuredNode

from config.attribute_settings import ATTRIBUTES_CONFIG
from config.attributes_mapping import AttributeMapping
from models.aton.nodes.organization import Organization
from models.portico import PPProv
import logging

log = logging.getLogger(__name__)


def get_provider_attributes(provider:PPProv, organization: Organization):
    for attribute in provider.attributes:
        attribute_fields: dict[str, Any] = {}
        # log.info(f"Attribute Id: {attribute.attribute_id}")
        # attribute_id = attribute.attribute_id
        # if str(attribute_id) == "502" or str(attribute_id) == "101278":
        #     mapping = ATTRIBUTES_CONFIG["provider"][str(attribute.attribute_id)]
        #     log.info(f"Mapping: {mapping}")
        for value in attribute.values:
            field_id = str(value.field_id)
            if value.value_date:
                attribute_fields[field_id] = value.value_date
            elif value.value_number:
                attribute_fields[field_id] = value.value_number
            else:
                attribute_fields[field_id] = value.value
        log.info(f"Attribute Fields: {attribute_fields}")
        attribute_id = attribute.attribute_id
        if str(attribute_id) == "502" or str(attribute_id) == "101278":
            mapping = ATTRIBUTES_CONFIG["provider"][str(attribute.attribute_id)]
            log.info(f"Mapping: {mapping}")
            node: StructuredNode = build_node_for_attribute(mapping, attribute_fields)
            log.info(f"Node: {node}")


def build_node_for_attribute(mapping:AttributeMapping,
                             attribute_fields: dict[str, Any]) -> StructuredNode:
    props = {}
    for field_id, field_value in attribute_fields.items():
        if field_id in mapping.ignore:
            continue
        if field_id in mapping.fields:
            aton_prop = mapping.fields[field_id]
            props[aton_prop] = field_value

    props.update(mapping.adornments)

    node_instance = mapping.node_class(**props)
    return node_instance