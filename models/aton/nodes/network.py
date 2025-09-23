from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty

from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.pp_net import PPNet


class Network(MockDataTest):
    code = StringProperty(required=True)
    name = StringProperty(required=True)
    isVendorNetwork = BooleanProperty(required=False)
    isHNETNetwork = BooleanProperty(required=False)

    product = RelationshipTo("models.aton.nodes.product.Product", "PART_OF")
    pp_net = RelationshipFrom("models.aton.nodes.pp_net.PPNet", "SOURCES")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_portico_source: PPNet | None = None

    def set_portico_source(self, source: PPNet):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source