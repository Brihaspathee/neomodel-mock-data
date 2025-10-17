from typing import Any

from neomodel import StringProperty, RelationshipTo, BooleanProperty

from models.aton.nodes.base_node import BaseNode


class Network(BaseNode):
    code = StringProperty(required=True)
    name = StringProperty(required=True)
    isVendorNetwork = BooleanProperty(required=False)
    isHNETNetwork = BooleanProperty(required=False)

    product = RelationshipTo("models.aton.nodes.product.Product", "PART_OF")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.LegacySystemIdentifier", "HAS_LEGACY_SYSTEM_IDENTIFIER")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None