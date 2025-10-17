import weakref

from models.aton.nodes.identifier import Identifier, NPI, DEA_Number, MedicareID, MedicaidID, LegacySystemIdentifier
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance


class PractitionerContext:

    def __init__(self, practitioner:Practitioner):
        self.practitioner = weakref.proxy(practitioner)
        self._portico_source: LegacySystemIdentifier | None = None
        self._identifiers = {
            "npi": [],
            "medicare_id": [],
            "medicaid_id": [],
            "dea_number": [],
            "legacy_system_id": []
        }
        self._qualifications: list[Qualification] = []
        self._role_instance: RoleInstance | None = None

    def add_identifier(self, identifier: Identifier):
        if isinstance(identifier, NPI):
            self._identifiers["npi"].append(identifier)
        elif isinstance(identifier, DEA_Number):
            self._identifiers["dea_number"].append(identifier)
        elif isinstance(identifier, MedicareID):
            self._identifiers["medicare_id"].append(identifier)
        elif isinstance(identifier, MedicaidID):
            self._identifiers["medicaid_id"].append(identifier)
        elif isinstance(identifier, LegacySystemIdentifier):
            self._identifiers["legacy_system_id"].append(identifier)
        else:
            ValueError(f"{identifier} is not a valid identifier")

    def get_identifiers(self):
        return self._identifiers

    def add_qualification(self, qualification: Qualification):
        self._qualifications.append(qualification)

    def get_qualifications(self):
        return self._qualifications

    def set_role_instance(self, role_instance: RoleInstance):
        self._role_instance = role_instance

    def get_role_instance(self):
        return self._role_instance

    def set_portico_source(self, source: LegacySystemIdentifier):
        self._portico_source = source

    def get_portico_source(self):
        return self._portico_source