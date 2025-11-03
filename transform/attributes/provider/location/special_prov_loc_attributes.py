import datetime
import logging

from models.aton.context.accessibility_context import AccessibilityContext
from models.aton.nodes.accessibility import Accessibility
from models.aton.nodes.validation import Validation
from models.aton.relationships.has_panel import HasPanel
from models.portico import PPProvTinLoc, PPProvLocAttrib
from transform.transform_utils import is_portico_loc_and_aton_loc_match

log = logging.getLogger(__name__)

def transform_panel_attr(**kwargs):
    prov_loc_attrib = kwargs.get("prov_loc_attrib")
    role_instance = kwargs.get("role_instance")
    prov_tin_loc: PPProvTinLoc = kwargs.get("prov_tin_loc")
    log.debug("Transforming panel question attribute")
    for role_network in role_instance.context.get_rns():
        for assoc_rl in role_network.context.get_assoc_rls():
            if is_portico_loc_and_aton_loc_match(prov_tin_loc, assoc_rl.role_location.context.get_location()):
                role_location = assoc_rl.role_location
                if role_location.context.get_location().context.get_accessibility():
                    accessibility = role_location.context.get_location().context.get_accessibility()
                else:
                    accessibility = Accessibility()
                    accessibility.context = AccessibilityContext()
                    role_location.context.get_location().context.set_accessibility(accessibility)
                if assoc_rl.panel_edge:
                    has_panel: HasPanel = assoc_rl.panel_edge
                else:
                    has_panel: HasPanel = HasPanel()
                _process_panel_questions_attribute(prov_loc_attrib,
                                                   has_panel,
                                                   accessibility)
                assoc_rl.panel_edge = has_panel

def _process_panel_questions_attribute(prov_loc_attrib: PPProvLocAttrib,
                                       has_panel: HasPanel,
                                       accessibility:Accessibility):
    for value in prov_loc_attrib.values:
        if value.field_id == 100309 and value.value == "Y":
            has_panel.status = "ACCEPTING_NEW_PATIENTS"
        elif value.field_id == 100310 and value.value == "Y":
            has_panel.status = "EXISTING_PATIENTS"
        elif value.field_id == 100311 and value.value == "Y":
            has_panel.status = "CLOSED"
        elif value.field_id == 102575 and value.value == "Y":
            accessibility.ada_basic_access = True
        elif value.field_id == 102576 and value.value == "Y":
            accessibility.ada_limited_access = True
        elif value.field_id == 102578 and value.value == "Y":
            accessibility.ada_parking = True
        elif value.field_id == 102579 and value.value == "Y":
            accessibility.ada_exterior_bldg = True
        elif value.field_id == 102580 and value.value == "Y":
            accessibility.ada_interior_bldg = True
        elif value.field_id == 102581 and value.value == "Y":
            accessibility.ada_restroom = True
        elif value.field_id == 102582 and value.value == "Y":
            accessibility.ada_exam_room = True
        elif value.field_id == 102583 and value.value == "Y":
            accessibility.ada_exam_table_scale = True
        elif value.field_id == 102584 and value.value == "Y":
            accessibility.ada_patient_area = True
        elif value.field_id == 106196 and value.value == "Y":
            accessibility.ada_patient_diagnostics = True
        elif value.field_id == 106215 and value.value == "Y":
            validation: Validation = Validation()
            accessibility_context: AccessibilityContext = accessibility.context
            validation.source = "Accessibility"
            validation.type = "Accessibility Validation"
            # validation.validation_date = datetime.date.today()
            accessibility_context.set_validation(validation)