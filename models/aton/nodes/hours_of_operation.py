from neomodel import StructuredNode, RelationshipFrom, JSONProperty

from models.aton.nodes.mock_data_test import MockDataTest


class HoursOfOperation(MockDataTest):
    hours = JSONProperty(required=True)

    contact = RelationshipFrom("models.aton.nodes.contact.Contact",
                               "HOURS_OF_OPERATION_ARE")