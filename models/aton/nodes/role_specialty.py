from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode


class RoleSpecialty(BaseNode):
    specialty: str = StringProperty(required=True)
    taxonomyCode: str = StringProperty(required=False)

    # Incoming relationships
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance",
                                     "SPECIALIZES")

    # Outgoing relationships
    role_locations = RelationshipTo("models.aton.nodes.role_location.RoleLocation",
                                         "PRACTICED_AT")

    prac_primary_specialty = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance",
                                     "PRIMARY_SPECIALTY_IS")

    _isPrimary = False  # internal transient field

    @property
    def isPrimary(self):
        return self._isPrimary

    @isPrimary.setter
    def isPrimary(self, value: bool):
        self._isPrimary = value

    def __str__(self):
        return (f"<RoleSpecialty:("
                f"specialty={self.specialty}, "
                f"taxonomyCode={self.taxonomyCode}, "
                f"isPrimary={self.isPrimary})>")



