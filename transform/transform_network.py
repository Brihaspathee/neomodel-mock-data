from models.aton.nodes.network import Network
from models.aton.nodes.product import Product
from models.portico.pp_net import PPNetDict
from transform.transformers import transform_to_aton
import logging

from models.portico import PPNet

log = logging.getLogger(__name__)

@transform_to_aton.register(PPNet)
def _(pp_net:PPNet) -> Product:
    net_dict: PPNetDict = pp_net.to_dict()
    product: Product = Product(
        code=net_dict["id"],
        name=net_dict["name"])
    networks: list[PPNetDict] = net_dict["children"]
    # log.info(f"Product {product.code}, it has {len(networks)} networks")
    for network in networks:
        net: Network = Network(
            code=network["id"],
            name=network["name"]
        )
        product.add_network(net)
    return product