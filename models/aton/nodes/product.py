from typing import Any

from neomodel import StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.base_node import BaseNode


class Product(BaseNode):
    code = StringProperty(required=True)
    name = StringProperty(required=True)

    network = RelationshipFrom("models.aton.nodes.network.Network", "PART_OF")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.LegacySystemIdentifier", "HAS_LEGACY_SYSTEM_IDENTIFIER")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context: Any = None

    def __str__(self):
        return f"Product(code: {self.code}, name: {self.name})"