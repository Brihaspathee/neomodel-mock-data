from typing import Any

from neomodel import StructuredNode

from config.attribute_settings import ATTRIBUTES_CONFIG
from config.attributes_mapping import AttributeMapping
from models.aton.nodes.identifier import NPI, Identifier, PPGID
from models.aton.nodes.organization import Organization
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty
from models.portico import PPProv, PPProvTinLoc
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
        if str(attribute_id) == "502" or str(attribute_id) == "101278" or str(attribute_id) == "103277":
            mapping = ATTRIBUTES_CONFIG["provider"][str(attribute.attribute_id)]
            # log.info(f"Mapping: {mapping}")
            node = build_node_for_attribute(mapping, attribute_fields)
            # log.info(f"Node: {node}")
            # log.info(f"Node type: {type(node)}")
            # log.info(f"Is this Type NPI: {isinstance(node, Identifier):}")
            # log.info(f"Is this Type Qualification: {isinstance(node, Qualification):}")
            if isinstance(node, Identifier):
                if isinstance(node, PPGID):
                    log.info(f"This is a PPG ID {node.value}")
                    log.info(f"This is a PPG ID - capitated ppg {node.capitated_ppg}")
                    log.info(f"This is a PPG ID - PCP required  {node.pcp_required}")
                    log.info(f"This is a PPG ID - Parent PPG ID  {node.parent_ppg_id}")
                    if node.capitated_ppg == "Y":
                        organization.capitated = True
                    else:
                        organization.capitated = False
                    if node.pcp_required == "Y":
                        organization.pcp_practitioner_required = True
                    else:
                        organization.pcp_practitioner_required = False
                    if node.parent_ppg_id:
                        organization.parent_ppg_id = node.parent_ppg_id
                organization.add_identifier(node)
            elif isinstance(node, Qualification):
                organization.add_qualification(node)
            else:
                log.error(f"Unable to determine node type for attribute {attribute_id}")


def get_prov_loc_attributes(pprov: PPProv, pp_prov_tin_loc:PPProvTinLoc, role_location:RoleLocation):
    for prov_loc_attr in pprov.loc_attributes:
        location: PPProvTinLoc = prov_loc_attr.location
        if location.id == pp_prov_tin_loc.id:
            attribute_id = prov_loc_attr.attribute_id
            attribute_fields: dict[str, Any] = {}
            for value in prov_loc_attr.values:
                field_id = str(value.field_id)
                if value.value_date:
                    attribute_fields[field_id] = value.value_date
                elif value.value_number:
                    attribute_fields[field_id] = value.value_number
                elif value.value:
                    attribute_fields[field_id] = value.value
            mapping = ATTRIBUTES_CONFIG["prov_loc"][str(attribute_id)]
            log.info(f"Mapping: {mapping}")
            log.info(f"Attribute Fields: {attribute_fields}")
            node = build_node_for_attribute(mapping, attribute_fields)
            log.info(f"Created Node for prov loc attribute: {node}")
            if isinstance(node, RoleSpecialty):
                role_location.add_specialty(node)



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
    log.info(f"Aton Properties: {props}")
    log.info(f"Aton Node Class: {mapping.node_class}")
    node_instance = mapping.node_class(**props)
    return node_instance