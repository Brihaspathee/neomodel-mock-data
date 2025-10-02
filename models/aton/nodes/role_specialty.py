from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode


class RoleSpecialty(BaseNode):
    specialty: str = StringProperty(required=True)
    taxonomy: str = StringProperty(required=False)

    # Incoming relationships
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance",
                                     "SPECIALIZES")

    # Outgoing relationships
    role_locations = RelationshipTo("models.aton.nodes.role_location.RoleLocation",
                                         "PRACTICED_AT")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isPrimary: str = "N"  # transient attribute
