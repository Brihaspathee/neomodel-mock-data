from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.validation import Validation


class Location(BaseNode):

    name: str = StringProperty(required=True)
    street_address: str = StringProperty(required=True)
    secondary_address: str = StringProperty(required=False)
    city: str = StringProperty(required=True)
    state: str = StringProperty(required=True)
    zip_code: str = StringProperty(required=True)
    county: str = StringProperty(required=False)
    county_fips: str = StringProperty(required=False)
    latitude: str = StringProperty(required=False)
    longitude: str = StringProperty(required=False)

    validation = RelationshipFrom("models.aton.nodes.validation.Validation", "VALIDATED")
    role_locations = RelationshipFrom("models.aton.nodes.role_location.RoleLocation", "LOCATION_IS")

    qualifications = RelationshipTo("models.aton.nodes.qualification.Qualification",
                                    "HAS_QUALIFICATION")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")
    pp_prov_tin_loc = RelationshipTo("models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC", "SOURCES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_validation: Validation | None = None
        self._portico_source: LegacySystemID | None = None
        self._pending_qualifications: list[Qualification] = []

    def __repr__(self):
        return f"{self.name} - {self.street_address} - {self.city} - {self.state} - {self.zip_code}"

    def set_pending_validation(self, validation: Validation):
        self._pending_validation = validation

    def get_pending_validation(self) -> Validation:
        return self._pending_validation

    def set_portico_source(self, portico_source: LegacySystemID):
        self._portico_source = portico_source

    def get_portico_source(self) -> LegacySystemID:
        return self._portico_source

    def add_pending_qualification(self, qualification: Qualification):
        self._pending_qualifications.append(qualification)

    def get_pending_qualifications(self) -> list[Qualification]:
        return self._pending_qualifications