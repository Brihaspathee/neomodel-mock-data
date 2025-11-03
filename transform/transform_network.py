from models.aton.context.network_context import NetworkContext
from models.aton.context.product_context import ProductContext
from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.network import Network
from models.aton.nodes.product import Product
from models.portico.pp_net import PPNetDict
from transform.transformers import transform_to_aton
from transform.attributes.transform_attribute import transform_attributes
import logging

from models.portico import PPNet

log = logging.getLogger(__name__)

@transform_to_aton.register(PPNet)
def _(pp_net:PPNet) -> Product:
    net_dict: PPNetDict = pp_net.to_dict()
    product: Product = Product(
        code=net_dict["id"],
        name=net_dict["description"])
    product.context = ProductContext()
    portico_prod: LegacySystemIdentifier = LegacySystemIdentifier(value= net_dict["id"],
                                                                  system="PORTICO",
                                                                  systemIdType="NET ID"
                                                                  )
    product.context.set_portico_source(portico_prod)
    networks: list[PPNetDict] = net_dict["children"]
    # log.debug(f"Product {product.code}, it has {len(networks)} networks")
    for network in networks:
        net: Network = Network(
            code=network["id"],
            name=network["description"]
        )
        net.context = NetworkContext()
        transform_attributes("NETWORK", network, net)
        log.debug(f"Is this a vendor network: {net.isVendorNetwork}")
        log.debug(f"Is this a health network: {net.isHNETNetwork}")
        portico_net: LegacySystemIdentifier = LegacySystemIdentifier(value=network["id"],
                                                                     system="PORTICO",
                                                                     systemIdType="NET ID")
        net.context.set_portico_source(portico_net)
        product.context.add_network(net)
    return product