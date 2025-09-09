from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo


class RoleSpecialty(StructuredNode):
    specialty: str = StringProperty(required=True)

    # Incoming relationships
    role_instance = RelationshipFrom("models.aton.nodes.role_instance.RoleInstance",
                                     "SPECIALIZES")

    # Outgoing relationships
    role_locations = RelationshipTo("models.aton.nodes.role_location.RoleLocation",
                                         "PRACTICED_AT")
