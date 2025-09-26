from neomodel import StructuredNode, RelationshipFrom, JSONProperty

from models.aton.nodes.base_node import BaseNode


class HoursOfOperation(BaseNode):
    hours = JSONProperty(required=True)

    contact = RelationshipFrom("models.aton.nodes.contact.Contact",
                               "HOURS_OF_OPERATION_ARE")