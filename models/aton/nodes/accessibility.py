from typing import Any

from neomodel import BooleanProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Accessibility(BaseNode):
    ada_basic_access: bool = BooleanProperty(required=False, db_property='adaBasicAccess')
    ada_limited_access: bool = BooleanProperty(required=False, db_property='adaLimitedAccess')
    ada_parking: bool = BooleanProperty(required=False, db_property='adaParking')
    ada_exterior_bldg: bool = BooleanProperty(required=False, db_property='adaExteriorBldg')
    ada_interior_bldg: bool = BooleanProperty(required=False, db_property='adaInteriorBldg')
    ada_restroom: bool = BooleanProperty(required=False, db_property='adaRestroom')
    ada_exam_room: bool = BooleanProperty(required=False, db_property='adaExamRoom')
    ada_exam_table_scale: bool = BooleanProperty(required=False, db_property='adaExamTableScale')
    ada_patient_area: bool = BooleanProperty(required=False, db_property='adaPatientArea')
    ada_patient_diagnostics: bool = BooleanProperty(required=False, db_property='adaPatientDiagnostics')

    location = RelationshipFrom("models.aton.nodes.location.Location",
                                    "ACCESSIBLE")
    validation = RelationshipFrom("models.aton.nodes.validation.Validation", "VALIDATED")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None