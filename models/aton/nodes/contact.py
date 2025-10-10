from typing import Any

from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.address import Address
from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.hours_of_operation import HoursOfOperation
from models.aton.nodes.telecom import Telecom


class Contact(BaseNode):
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

    hours_of_operation = RelationshipTo(
        "models.aton.nodes.hours_of_operation.HoursOfOperation",
        "HOURS_OF_OPERATION_ARE")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None