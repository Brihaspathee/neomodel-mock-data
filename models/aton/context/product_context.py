import weakref

from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.network import Network
from models.aton.nodes.product import Product


class ProductContext:
    def __init__(self):
        # self.product = weakref.proxy(product)
        self._networks: list[Network] = []
        self._portico_source: LegacySystemIdentifier | None = None

    def add_network(self, network: Network):
        self._networks.append(network)

    def get_networks(self) -> list[Network]:
        return self._networks

    def set_portico_source(self, source: LegacySystemIdentifier):
        self._portico_source = source

    def get_portico_source(self):
        return self._portico_source
