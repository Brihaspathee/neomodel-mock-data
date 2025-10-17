from typing import Any

from neomodel import StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode


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
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.LegacySystemIdentifier", "HAS_LEGACY_SYSTEM_IDENTIFIER")
    pp_prov_tin_loc = RelationshipTo("models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC", "SOURCES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None

    def __repr__(self):
        return f"{self.name} - {self.street_address} - {self.city} - {self.state} - {self.zip_code}"