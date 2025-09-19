from neomodel import StructuredNode, StringProperty, RelationshipTo


class PPNet(StructuredNode):
    __label__ = "PP_Net"
    net_id = StringProperty(required=True)

    aton_net = RelationshipTo("models.aton.nodes.network.Network", "SOURCES")
    aton_prod = RelationshipTo("models.aton.nodes.product.Product", "SOURCES")