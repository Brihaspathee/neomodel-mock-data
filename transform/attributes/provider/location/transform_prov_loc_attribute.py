import logging
from typing import Any

from config.attribute_settings import ATTRIBUTES_CONFIG
from models.aton.nodes.location import Location
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty
from models.portico import PPProv, PPProvTinLoc
from transform.attributes.transform_attribute_util import build_node_for_attribute

log = logging.getLogger(__name__)

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