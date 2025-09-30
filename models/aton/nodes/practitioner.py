from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, RelationshipTo, ArrayProperty

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.identifier import LegacySystemID, Identifier, NPI, DEA_Number, MedicareID, MedicaidID
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


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
    race: str = ArrayProperty(required=False)
    ethnicity: str = ArrayProperty(required=False)

    role = RelationshipTo("models.aton.nodes.role_instance.RoleInstance",
                          "HAS_ROLE")
    # Identifiers
    npi = RelationshipTo("models.aton.nodes.identifier.NPI", "HAS_NPI")
    dea_number = RelationshipTo("models.aton.nodes.identifier.DEA_Number", "HAS_DEA_NUMBER")
    medicare_id = RelationshipTo("models.aton.nodes.identifier.MedicareID", "HAS_MEDICARE_ID")
    medicaid_id = RelationshipTo("models.aton.nodes.identifier.MedicaidID", "HAS_MEDICAID_ID")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")

    # Qualifications
    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification",
                                    "HAS_QUALIFICATION")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for identifiers
        self._pending_identifiers = {
            "npi": [],
            "medicare_id": [],
            "medicaid_id": [],
            "dea_number":[],
            "legacy_system_id": []
        }

        self._pending_qualifications: list[Qualification] = []

        self._pending_role_instance: RoleInstance | None = None

        self._pending_portico_source: LegacySystemID | None = None


    def set_portico_source(self, source: LegacySystemID):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source

    def set_pending_role_instance(self, role_instance: RoleInstance):
        self._pending_role_instance = role_instance

    def get_pending_role_instance(self):
        return self._pending_role_instance

    def add_identifier(self, identifier:Identifier):
        if isinstance(identifier, NPI):
            self._pending_identifiers["npi"].append(identifier)
        elif isinstance(identifier, DEA_Number):
            self._pending_identifiers["dea_number"].append(identifier)
        elif isinstance(identifier, MedicareID):
            self._pending_identifiers["medicare_id"].append(identifier)
        elif isinstance(identifier, MedicaidID):
            self._pending_identifiers["medicaid_id"].append(identifier)
        elif isinstance(identifier, LegacySystemID):
            self._pending_identifiers["legacy_system_id"].append(identifier)
        else:
            ValueError(f"{identifier} is not a valid identifier")

    def get_pending_identifiers(self):
        return self._pending_identifiers

    def add_qualification(self, qualification:Qualification):
        self._pending_qualifications.append(qualification)

    def get_pending_qualifications(self):
        return self._pending_qualifications