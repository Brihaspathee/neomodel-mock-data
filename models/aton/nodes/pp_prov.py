from neomodel import StructuredNode, StringProperty, RelationshipTo

from models.aton.nodes.mock_data_test import MockDataTest


class PP_PROV(MockDataTest):
    # __label__ = "PP_PROV"
    prov_id = StringProperty(required=True)

    aton_org = RelationshipTo("models.aton.nodes.organization.Organization", "SOURCES")