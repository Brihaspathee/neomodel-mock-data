from neomodel import StructuredNode, StringProperty, RelationshipTo


class PPNet(StructuredNode):
    __label__ = "PP_Net"
    net_id = StringProperty(required=True)

    aton_net_prod = RelationshipTo("models.aton.nodes.network.Network", "SOURCES")