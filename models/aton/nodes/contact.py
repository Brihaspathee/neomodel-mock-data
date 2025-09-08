from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.address import Address


class Contact(StructuredNode):
    use = StringProperty(required=True)

    role_location = RelationshipFrom(
        "models.aton.nodes.role_location.RoleLocation",
        "HAS_LOCATION_CONTACT")

    organization = RelationshipFrom(
        "models.aton.nodes.organization.Organization",
        "HAS_ORGANIZATION_CONTACT"
    )

    address = RelationshipTo(
        "models.aton.nodes.address.Address","ADDRESS_IS" )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for identifiers
        self._pending_address: Address | None = None

    def set_address(self, address: Address):
        self.address = address

    def get_address(self):
        return self.address