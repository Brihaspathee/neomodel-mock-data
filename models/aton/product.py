from neomodel import StructuredNode, StringProperty, RelationshipFrom

from models.aton.network import Network


class Product(StructuredNode):
    code = StringProperty(required=True)
    name = StringProperty(required=True)

    network = RelationshipFrom("models.aton.network.Network", "PART_OF")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pending_networks: list[Network] = []

    def add_network(self, network: Network):
        self._pending_networks.append(network)

    def get_pending_networks(self) -> list[Network]:
        return self._pending_networks

    def __str__(self):
        return f"Product(code: {self.code}, name: {self.name})"