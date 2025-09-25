from neomodel import StructuredNode, StringProperty, RelationshipFrom, RelationshipTo

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.network import Network
from models.aton.nodes.pp_net import PP_NET


class Product(MockDataTest):
    code = StringProperty(required=True)
    name = StringProperty(required=True)

    network = RelationshipFrom("models.aton.nodes.network.Network", "PART_OF")
    legacy_system_id = RelationshipTo("models.aton.nodes.identifier.Identifier", "HAS_LEGACY_SYSTEM_ID")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_networks: list[Network] = []
        self._pending_portico_source: LegacySystemID | None = None

    def add_network(self, network: Network):
        self._pending_networks.append(network)

    def get_pending_networks(self) -> list[Network]:
        return self._pending_networks

    def set_portico_source(self, source: LegacySystemID):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source

    def __str__(self):
        return f"Product(code: {self.code}, name: {self.name})"