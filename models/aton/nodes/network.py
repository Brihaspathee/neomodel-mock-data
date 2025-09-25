from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.pp_net import PP_NET


class Network(MockDataTest):
    code = StringProperty(required=True)
    name = StringProperty(required=True)
    isVendorNetwork = BooleanProperty(required=False)
    isHNETNetwork = BooleanProperty(required=False)

    product = RelationshipTo("models.aton.nodes.product.Product", "PART_OF")
    pp_net = RelationshipFrom("models.aton.nodes.pp_net.PP_NET", "SOURCES")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_portico_source: LegacySystemID | None = None

    def set_portico_source(self, source: LegacySystemID):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source