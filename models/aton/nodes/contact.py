from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.address import Address
from models.aton.nodes.telecom import Telecom


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

    telecom = RelationshipTo(
        "models.aton.nodes.telecom.Telecom", "TELECOM_IS")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Temporary storage for identifiers
        self._pending_address: Address | None = None
        self._pending_telecom: Telecom | None = None

    def set_pending_address(self, address: Address):
        self._pending_address = address

    def get_pending_address(self):
        return self._pending_address

    def set_pending_telecom(self, telecom: Telecom):
        self._pending_telecom = telecom

    def get_pending_telecom(self):
        return self._pending_telecom