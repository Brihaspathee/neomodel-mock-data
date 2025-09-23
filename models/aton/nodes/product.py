from neomodel import StructuredNode, StringProperty, RelationshipFrom

from models.aton.nodes.mock_data_test import MockDataTest
from models.aton.nodes.network import Network
from models.aton.nodes.pp_net import PPNet


class Product(MockDataTest):
    code = StringProperty(required=True)
    name = StringProperty(required=True)

    network = RelationshipFrom("models.aton.nodes.network.Network", "PART_OF")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_networks: list[Network] = []
        self._pending_portico_source: PPNet | None = None

    def add_network(self, network: Network):
        self._pending_networks.append(network)

    def get_pending_networks(self) -> list[Network]:
        return self._pending_networks

    def set_portico_source(self, source: PPNet):
        self._pending_portico_source = source

    def get_portico_source(self):
        return self._pending_portico_source

    def __str__(self):
        return f"Product(code: {self.code}, name: {self.name})"