from neomodel import StructuredNode, StringProperty, RelationshipFrom

from models.aton.nodes.pp_prov_tin_loc import PPProvTINLoc
from models.aton.nodes.validation import Validation


class Location(StructuredNode):

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

    pp_prov_tin_loc = RelationshipFrom("models.aton.nodes.pp_prov_tin_loc.PPProvTINLoc", "SOURCES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_validation: Validation | None = None
        self._portico_source: PPProvTINLoc | None = None

    def __repr__(self):
        return f"{self.name} - {self.street_address} - {self.city} - {self.state} - {self.zip_code}"

    def set_pending_validation(self, validation: Validation):
        self._pending_validation = validation

    def get_pending_validation(self) -> Validation:
        return self._pending_validation

    def set_portico_source(self, portico_source: PPProvTINLoc):
        self._portico_source = portico_source

    def get_portico_source(self) -> PPProvTINLoc:
        return self._portico_source