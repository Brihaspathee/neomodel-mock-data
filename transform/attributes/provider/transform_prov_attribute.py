from typing import Any

from models.aton.context.ppg_id_context import PPGIDContext
from models.aton.nodes.identifier import Identifier, PPGID
from models.aton.nodes.organization import Organization
from config.attribute_settings import ATTRIBUTES_CONFIG, SPECIAL_ATTRIBUTES
from models.aton.nodes.qualification import Qualification
from models.portico import PPProv
import logging

from transform.attributes.transform_attribute_util import build_node_for_attribute, transform_special_attribute

log = logging.getLogger(__name__)

def get_provider_attributes(provider:PPProv, organization: Organization):
    log.debug(f"Special Attributes: {SPECIAL_ATTRIBUTES}")
    for attribute in provider.attributes:
        if str(attribute.attribute_id) in SPECIAL_ATTRIBUTES:
            transform_special_attribute(attribute.attribute_id, attribute, organization)
            continue
        attribute_fields: dict[str, Any] = {}
        for value in attribute.values:
            field_id = str(value.field_id)
            if value.value_date:
                attribute_fields[field_id] = value.value_date
            elif value.value_number:
                attribute_fields[field_id] = value.value_number
            else:
                attribute_fields[field_id] = value.value
        log.debug(f"Attribute Fields: {attribute_fields}")
        attribute_id = attribute.attribute_id
        # if str(attribute_id) == "502" or str(attribute_id) == "101278" or str(attribute_id) == "103277":
        mapping = ATTRIBUTES_CONFIG["provider"][str(attribute.attribute_id)]
        # log.debug(f"Mapping: {mapping}")
        node = build_node_for_attribute(mapping, attribute_fields)
        # log.debug(f"Node: {node}")
        # log.debug(f"Node type: {type(node)}")
        # log.debug(f"Is this Type NPI: {isinstance(node, Identifier):}")
        # log.debug(f"Is this Type Qualification: {isinstance(node, Qualification):}")
        if isinstance(node, Identifier):
            is_identifier_added = False
            if isinstance(node, PPGIDContext):
                log.debug(f"This is a PPG ID {node.value}")
                log.debug(f"This is a PPG ID - capitated ppg {node.capitated_ppg}")
                log.debug(f"This is a PPG ID - PCP required  {node.pcp_required}")
                log.debug(f"This is a PPG ID - Parent PPG ID  {node.parent_ppg_id}")
                if node.capitated_ppg == "Y":
                    organization.capitated = True
                else:
                    organization.capitated = False
                if node.pcp_required == "Y":
                    organization.pcp_practitioner_required = True
                else:
                    organization.pcp_practitioner_required = False
                if node.parent_ppg_id:
                    organization.context.set_parent_ppg_id(node.parent_ppg_id)
                ppg_id = PPGID(value=node.value)
                organization.context.add_identifier(ppg_id)
                is_identifier_added = True
            # # if identifier is a PPG ID, then it would have been added above
            # # else add it to the organization
            if not is_identifier_added:
                organization.context.add_identifier(node)
        elif isinstance(node, Qualification):
            organization.context.add_qualification(node)
        else:
            log.error(f"Unable to determine node type for attribute {attribute_id}")