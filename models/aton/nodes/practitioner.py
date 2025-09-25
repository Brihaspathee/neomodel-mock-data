from neo4j.time import DateType
from neomodel import StringProperty, DateProperty, RelationshipTo

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.pp_prac import PP_PRAC
from models.aton.nodes.role_instance import RoleInstance


class Practitioner(MockDataTest):
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
    race: str = StringProperty(required=False)
    ethnicity: str = StringProperty(required=False)

    role = RelationshipTo("models.aton.nodes.role_instance.RoleInstance",
                          "HAS_ROLE")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for identifiers
        # self._pending_identifiers = {
        #     "npi": [],
        #     "tin": [],
        #     "medicare_id": [],
        #     "medicaid_id": [],
        #     "ppg_id": []
        # }

        # self._pending_qualifications: list[Qualification] = []

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