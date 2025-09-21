from neomodel import StructuredNode, RelationshipFrom, JSONProperty


class HoursOfOperation(StructuredNode):
    hours = JSONProperty(required=True)

    contact = RelationshipFrom("models.aton.nodes.contact.Contact",
                               "HOURS_OF_OPERATION_ARE")