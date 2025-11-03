import logging
from typing import Any

from config.attribute_settings import ATTRIBUTES_CONFIG, SPECIAL_ATTRIBUTES
from models.aton.context.age_limitation_helper import AgeLimitationHelper
from models.aton.nodes.location import Location
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty
from models.aton.relationships.has_panel import HasPanel
from models.portico import PPProv, PPProvTinLoc
from transform.attributes.transform_attribute_util import build_node_for_attribute, transform_special_attribute
from transform.transform_utils import is_aton_locs_match
from utils.common_utils import merge_objects

log = logging.getLogger(__name__)

def get_prov_loc_attributes(pprov: PPProv, pp_prov_tin_loc:PPProvTinLoc, role_location:RoleLocation, role_instance:RoleInstance):
    for prov_loc_attr in pprov.loc_attributes:
        portico_location: PPProvTinLoc = prov_loc_attr.location
        if str(prov_loc_attr.attribute_id) in SPECIAL_ATTRIBUTES:
            transform_special_attribute(prov_loc_attr.attribute_id, prov_loc_attr, role_instance, portico_location)
            continue
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
                role_location.context.add_specialty(node)
            if isinstance(node, Qualification):
                qualification: Qualification = node
                if qualification.type == "DHSSE Certification":
                    if qualification.status == "P":
                        qualification.status = "PASSED"
                    elif qualification.status == "C":
                        qualification.status = "CANCELLED"
                aton_location:Location = role_location.context.get_location()
                aton_location.context.add_qualification(qualification)
            if isinstance(node, HasPanel) or isinstance(node, AgeLimitationHelper):
                _process_panel_questions_attribute(node, role_instance, role_location)



def _process_age_limitation_attr(has_panel, node):
    if node.lowest_units is not None and node.lowest_age is not None:
        if node.lowest_units == 'Y':
            has_panel.lowest_age_years = node.lowest_age
        elif node.lowest_units == 'M':
            has_panel.lowest_age_months = node.lowest_age
    if node.highest_units is not None and node.highest_age is not None:
        if node.highest_units == 'Y':
            has_panel.highest_age_years = node.highest_age
        elif node.lowest_units == 'M':
            has_panel.highest_age_months = node.highest_age

def _process_panel_questions_attribute(panel_data, role_instance, role_location):
    for role_network in role_instance.context.get_rns():
        for assoc_rl in role_network.context.get_assoc_rls():
            if is_aton_locs_match(role_location.context.get_location(), assoc_rl.role_location.context.get_location()):
                if assoc_rl.panel_edge:
                    has_panel: HasPanel = assoc_rl.panel_edge
                    final_panel_data: HasPanel | None = None
                    if isinstance(panel_data, HasPanel):
                        merged_has_panel = merge_objects(has_panel, panel_data, False)
                        final_panel_data = merged_has_panel
                        # assoc_panel: AssociatedPanel = AssociatedPanel(role_location=role_location,
                        #                                                panel_edge=final_panel_data)
                        # role_network.context.set_panel(assoc_panel)
                    elif isinstance(panel_data, AgeLimitationHelper):
                        _process_age_limitation_attr(has_panel, panel_data)
                        final_panel_data = has_panel
                    assoc_rl.panel_edge = final_panel_data

                else:
                    final_panel_data: HasPanel | None = panel_data
                    if isinstance(panel_data, AgeLimitationHelper):
                        has_panel: HasPanel = HasPanel()
                        _process_age_limitation_attr(has_panel, panel_data)
                        final_panel_data = has_panel
                    assoc_rl.panel_edge = final_panel_data

