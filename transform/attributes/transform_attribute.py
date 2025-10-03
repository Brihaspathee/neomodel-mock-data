from typing import Any

from neomodel import StructuredNode

from config.attribute_settings import ATTRIBUTES_CONFIG
from config.attributes_mapping import AttributeMapping
from models.aton.nodes.identifier import NPI, Identifier, PPGID
from models.aton.nodes.location import Location
from models.aton.nodes.network import Network
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty
from models.portico import PPProv, PPProvTinLoc, PPNet, PPPrac
import logging

from models.portico.pp_net import PPNetDict
from transform.attributes.practitioner.transform_prac_attributes import transform_prac_node, \
    transform_prac_loc_attributes

log = logging.getLogger(__name__)

def get_net_attributes(pp_net:PPNetDict, network:Network):
    log.debug(f"Network type: {type(pp_net)}")
    log.debug(f"Network Attributes: {pp_net.get('attributes')}")
    for attribute in pp_net.get('attributes', []):
        log.debug(f"Attribute: {attribute.get('attribute_id')}")
        try:
            attr_mapping = ATTRIBUTES_CONFIG["network"][attribute.get('attribute_id')]
            # Load the attribute only if a mapping is present
            # else do not load the attribute
            attribute_fields: dict[str, Any] = {}
            for value in attribute.get("values", []):
                field_id = str(value.get("field_id"))
                attribute_fields[field_id] = value.get("value")
                if attribute.get("attribute_type") == "NET_IS_VENDOR" and value.get("value") == "Y":
                    network.isVendorNetwork = True
                elif attribute.get("attribute_type") == "NET_HEALTHNET" and value.get("value") == "Y":
                    network.isHNETNetwork = True
        except KeyError:
            log.debug(f"No mapping found for attribute {attribute.get('attribute_id')}, hence it will not be loaded")

def get_provider_attributes(provider:PPProv, organization: Organization):
    for attribute in provider.attributes:
        attribute_fields: dict[str, Any] = {}
        # log.debug(f"Attribute Id: {attribute.attribute_id}")
        # attribute_id = attribute.attribute_id
        # if str(attribute_id) == "502" or str(attribute_id) == "101278":
        #     mapping = ATTRIBUTES_CONFIG["provider"][str(attribute.attribute_id)]
        #     log.debug(f"Mapping: {mapping}")
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
            if isinstance(node, PPGID):
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
                    organization.parent_ppg_id = node.parent_ppg_id
            organization.add_identifier(node)
        elif isinstance(node, Qualification):
            organization.add_qualification(node)
        else:
            log.error(f"Unable to determine node type for attribute {attribute_id}")


def get_prac_attributes(pp_prac:PPPrac, practitioner:Practitioner):
    for attribute in pp_prac.attributes:
        attribute_fields: dict[str, Any] = {}
        for value in attribute.values:
            field_id = str(value.field_id)
            if value.value_date:
                attribute_fields[field_id] = value.value_date
            elif value.value_number:
                attribute_fields[field_id] = value.value_number
            else:
                attribute_fields[field_id] = value.value
        attribute_id = attribute.attribute_id
        mapping = ATTRIBUTES_CONFIG["practitioner"][str(attribute.attribute_id)]
        node = build_node_for_attribute(mapping, attribute_fields)
        if isinstance(node, Identifier):
            practitioner.add_identifier(node)
        elif isinstance(node, Qualification):
            practitioner.add_qualification(node)
        elif isinstance(node, Practitioner):
            log.debug(f"This is a Practitioner {node}")
            transform_prac_node(attribute_id, node, practitioner )
        else:
            log.error(f"Unable to determine node type for attribute {attribute_id}")

def get_prac_loc_attributes(pp_prac: PPPrac,
                            pp_prov_tin_loc: PPProvTinLoc,
                            prov_id: int,
                            role_instance:RoleInstance):
    for prac_loc_attr in pp_prac.loc_attributes:
        log.info(f"Prac Loc attribute id: {prac_loc_attr.id}")
        portico_location: PPProvTinLoc = prac_loc_attr.location
        prac_loc_prov_id: int = prac_loc_attr.prov_id
        log.debug(f"Portico Location Id {portico_location.id}")
        log.debug(f"Location Id {pp_prov_tin_loc.id}")
        log.debug(f"Location for specialty:{portico_location}")
        log.debug(f"Provider ID:{prac_loc_prov_id}")
        if portico_location.id == pp_prov_tin_loc.id and prov_id == prac_loc_prov_id:
            attribute_id = prac_loc_attr.attribute_id
            attribute_fields: dict[str, Any] = {}
            for value in prac_loc_attr.values:
                field_id = str(value.field_id)
                if value.value_date:
                    attribute_fields[field_id] = value.value_date
                elif value.value_number:
                    attribute_fields[field_id] = value.value_number
                elif value.value:
                    attribute_fields[field_id] = value.value
            mapping = ATTRIBUTES_CONFIG["prac_loc"][str(attribute_id)]
            log.debug(f"Mapping: {mapping}")
            log.debug(f"Attribute Fields: {attribute_fields}")
            node = build_node_for_attribute(mapping, attribute_fields)
            if isinstance(node, RoleSpecialty):
                log.debug(f"Role Specialty isPrimary {node.isPrimary}")
                role_instance.add_prac_rs(node)

def get_prov_loc_attributes(pprov: PPProv, pp_prov_tin_loc:PPProvTinLoc, role_location:RoleLocation):
    for prov_loc_attr in pprov.loc_attributes:
        portico_location: PPProvTinLoc = prov_loc_attr.location
        if portico_location.id == pp_prov_tin_loc.id:
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
            log.debug(f"Mapping: {mapping}")
            log.debug(f"Attribute Fields: {attribute_fields}")
            node = build_node_for_attribute(mapping, attribute_fields)
            log.debug(f"Created Node for prov loc attribute: {node}")
            if isinstance(node, RoleSpecialty):
                role_location.add_specialty(node)
            if isinstance(node, Qualification):
                qualification: Qualification = node
                if qualification.type == "DHSSE Certification":
                    if qualification.status == "P":
                        qualification.status = "PASSED"
                    elif qualification.status == "C":
                        qualification.status = "CANCELLED"
                aton_location:Location = role_location.get_location()
                aton_location.add_pending_qualification(qualification)



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
            aton_prop = mapping.fields[field_id]
            props[aton_prop] = field_value

    props.update(mapping.adornments)
    log.debug(f"Aton Properties: {props}")
    log.debug(f"Aton Node Class: {mapping.node_class}")
    node_instance = mapping.node_class(**props)
    log.debug(f"Node instance: {node_instance}")
    return node_instance

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
        field_id = condition["field_id"]
        operator = condition["operator"]
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