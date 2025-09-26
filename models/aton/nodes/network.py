from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.identifier import LegacySystemID


class Network(BaseNode):
    code = StringProperty(required=True)
    name = StringProperty(required=True)
    isVendorNetwork = BooleanProperty(required=False)
    isHNETNetwork = BooleanProperty(required=False)

    product = RelationshipTo("models.aton.nodes.product.Product", "PART_OF")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_portico_source: LegacySystemID | None = None

    def set_portico_source(self, source: LegacySystemID):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source