from typing import Any

from config.attribute_settings import ATTRIBUTES_CONFIG
from models.aton.nodes.disorder import Disorder
from models.aton.nodes.healthcare_service import HealthcareService
from models.aton.nodes.identifier import Identifier
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance
from models.portico import PPPrac, PPProvTinLoc

import logging

from transform.attributes.transform_attribute_util import build_node_for_attribute

log = logging.getLogger(__name__)


def get_prac_attributes(pp_prac:PPPrac, practitioner:Practitioner):
    ri: RoleInstance = practitioner.context.get_role_instance()
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
        if not node:
            log.debug(f"For Practitioner {pp_prac.fname}, a node for the attribute {attribute_id} could not be built")
            log.debug(f"Conditions for creating the node may not have been met")
            continue
        if isinstance(node, Identifier):
            practitioner.context.add_identifier(node)
        elif isinstance(node, Qualification):
            practitioner.context.add_qualification(node)
        elif isinstance(node, Practitioner):
            log.debug(f"This is a Practitioner {node}")
            transform_prac_node(attribute_id, node, practitioner )
        elif isinstance(node, Disorder):
            log.info(f"This is a Disorder {node}")
            ri.context.add_prac_disorders(node)
        elif isinstance(node, HealthcareService):
            log.info(f"This is a HealthcareService {node}")
            ri.context.add_prac_hs(node)
        else:
            log.error(f"Unable to determine node type for attribute {attribute_id}"
                      f"for practitioner {pp_prac.id} name is {pp_prac.fname}")

# def transform_prac_loc_attributes(pp_prac: PPPrac,
#                                   pp_prov_tin_loc: PPProvTinLoc,
#                                   prov_id: int,
#                             role_instance:RoleInstance):
#     pass


def transform_prac_node(attribute_id: int, source_prac: Practitioner, destination_prac: Practitioner):
    log.debug(f"Transforming attribute {attribute_id}")
    if attribute_id == 103877:
        destination_prac.altFirstName = source_prac.altFirstName
        destination_prac.middle_name = source_prac.middle_name
        destination_prac.altLastName = source_prac.altLastName
    elif attribute_id == 100039:
        if source_prac.race:
            if destination_prac.race is None:
                destination_prac.race = []
            destination_prac.race.append(source_prac.race)
        if source_prac.ethnicity:
            if destination_prac.ethnicity is None:
                destination_prac.ethnicity = []
            destination_prac.ethnicity.append(source_prac.ethnicity)
