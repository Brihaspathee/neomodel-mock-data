from neomodel import StructuredNode, StringProperty, RelationshipTo

from models.aton.nodes.mock_data_test import MockDataTest


class PP_NET(MockDataTest):
    # __label__ = "PP_Net"
    net_id = StringProperty(required=True)

    aton_net = RelationshipTo("models.aton.nodes.network.Network", "SOURCES")
    aton_prod = RelationshipTo("models.aton.nodes.product.Product", "SOURCES")