from neomodel import StructuredNode, RelationshipFrom, RelationshipTo

from models.aton.nodes.contact import Contact
from models.aton.nodes.location import Location
from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.role_specialty import RoleSpecialty
from models.aton.relationships.exclude_from_directory import ExcludeFromDirectory
from models.aton.relationships.has_panel import HasPanel
from models.aton.relationships.role_location_serves import RoleLocationServes


class RoleLocation(MockDataTest):
    # Relationships
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "PERFORMED_AT")
    location = RelationshipTo("models.aton.nodes.location.Location", "LOCATION_IS")
    contacts = RelationshipTo("models.aton.nodes.contact.Contact", "HAS_LOCATION_CONTACT")

    role_network = RelationshipTo("models.aton.nodes.role_network.RoleNetwork",
                                  "ROLE_LOCATION_SERVES",
                                  model=RoleLocationServes)
    rn_behavior_health = RelationshipFrom("models.aton.nodes.role_network.RoleNetwork",
                                          "BEHAVIOR_HEALTH")
    rn_pcp = RelationshipFrom("models.aton.nodes.role_network.RoleNetwork",
                              "PCP")
    rn_exclude_from_directory = RelationshipFrom("models.aton.nodes.role_network.RoleNetwork",
                                                 "EXCLUDE_FROM_DIRECTORY",
                                                 model=ExcludeFromDirectory)
    rn_has_panel = RelationshipFrom("models.aton.nodes.role_network.RoleNetwork",
                                    "HAS_PANEL",
                                    model=HasPanel)
    specialties = RelationshipTo("models.aton.nodes.role_specialty.RoleSpecialty", "PRACTICED_AT")

    primary_location = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance", "PRIMARY_LOCATION_IS")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._location: Location | None = None
        self._pending_contacts: list[Contact] = []
        self._pending_specialties: list[RoleSpecialty] = []
        self._is_primary: bool = False


    def set_location(self, location: Location):
        self._location = location

    def get_location(self) -> Location:
        return self._location

    def add_contact(self, contact: Contact):
        self._pending_contacts.append(contact)

    def get_pending_contacts(self) -> list[Contact]:
        return self._pending_contacts

    def add_specialty(self, specialty: RoleSpecialty):
        self._pending_specialties.append(specialty)

    def get_pending_specialties(self) -> list[RoleSpecialty]:
        return self._pending_specialties

    def set_is_primary(self, is_primary: bool):
        self._is_primary = is_primary

    def get_is_primary(self) -> bool:
        return self._is_primary