import weakref

from models.aton.nodes.contact import Contact
from models.aton.nodes.location import Location
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty


class RoleLocationContext:
    def __init__(self, role_location: RoleLocation):
        self.role_location = weakref.proxy(role_location)
        self._location: Location | None = None
        self._specialties: list[RoleSpecialty] = []
        self._contacts: list[Contact] = []
        self._is_primary: bool = False

    def set_location(self, location: Location):
        self._location = location

    def get_location(self) -> Location:
        return self._location

    def add_specialty(self, specialty: RoleSpecialty):
        self._specialties.append(specialty)

    def get_specialties(self) -> list[RoleSpecialty]:
        return self._specialties

    def add_contact(self, contact:Contact):
        """
        Adds a given contact to the `_contacts` list.
        """
        self._contacts.append(contact)

    def get_contacts(self):
        """
        Returns a list of contacts associated with the role location.
        """
        return self._contacts

    def set_is_primary(self, is_primary: bool):
        self._is_primary = is_primary

    def get_is_primary(self) -> bool:
        return self._is_primary