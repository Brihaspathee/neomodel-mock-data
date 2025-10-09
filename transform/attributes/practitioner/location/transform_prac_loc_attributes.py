import logging
from typing import Any

from config.attribute_settings import ATTRIBUTES_CONFIG
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_specialty import RoleSpecialty
from models.portico import PPPrac, PPProvTinLoc
from transform.attributes.transform_attribute_util import build_node_for_attribute

log = logging.getLogger(__name__)

def get_prac_loc_attributes(pp_prac: PPPrac,
                            pp_prov_tin_loc: PPProvTinLoc,
                            prov_id: int,
                            role_instance:RoleInstance):
    for prac_loc_attr in pp_prac.loc_attributes:
        log.debug(f"Prac Loc attribute id: {prac_loc_attr.id}")
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