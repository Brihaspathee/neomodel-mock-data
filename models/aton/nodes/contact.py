from neomodel import StructuredNode, StringProperty, RelationshipFrom


class Contact(StructuredNode):
    use = StringProperty(required=True)

    role_location = RelationshipFrom("models.aton.nodes.role_location.RoleLocation", "HAS_LOCATION_CONTACT")