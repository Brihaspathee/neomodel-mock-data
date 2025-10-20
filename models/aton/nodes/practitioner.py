from typing import Any

from neo4j.time._metaclasses import DateType
from neomodel import StringProperty, DateProperty, RelationshipTo, ArrayProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Practitioner(BaseNode):
    first_name: str = StringProperty(required=True)
    last_name: str = StringProperty(required=True)
    middle_name: str = StringProperty(required=False)
    birthDate: DateType = DateProperty(required=False)
    salutation: str = StringProperty(required=False)
    suffix: str = StringProperty(required=False)
    gender: str = StringProperty(required=False)
    ssn: str = StringProperty(required=False)
    altFirstName: str = StringProperty(required=False)
    altLastName: str = StringProperty(required=False)
    altMiddleName: str = StringProperty(required=False)
    race: list[str] = ArrayProperty(required=False)
    ethnicity: list[str] = ArrayProperty(required=False)

    role = RelationshipTo("models.aton.nodes.role_instance.RoleInstance",
                          "HAS_ROLE")
    # Identifiers
    npi = RelationshipTo("models.aton.nodes.identifier.NPI", "HAS_NPI")
    dea_number = RelationshipTo("models.aton.nodes.identifier.DEA_Number", "HAS_DEA_NUMBER")
    medicare_id = RelationshipTo("models.aton.nodes.identifier.MedicareID", "HAS_MEDICARE_ID")
    medicaid_id = RelationshipTo("models.aton.nodes.identifier.MedicaidID", "HAS_MEDICAID_ID")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.LegacySystemIdentifier", "HAS_LEGACY_SYSTEM_IDENTIFIER")

    # Qualifications
    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification",
                                    "HAS_QUALIFICATION")

    pp_prac = RelationshipFrom("models.aton.nodes.pp_prac.PP_PRAC", "SOURCES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None