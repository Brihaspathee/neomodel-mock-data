import models
from models.aton.nodes.network import Network
from models.aton.nodes.product import Product
from models.portico.pp_net import PPNetDict
from transform.transformers import transform_to_aton
from transform.transform_attribute import get_net_attributes
import logging

from models.portico import PPNet

log = logging.getLogger(__name__)

@transform_to_aton.register(PPNet)
def _(pp_net:PPNet) -> Product:
    net_dict: PPNetDict = pp_net.to_dict()
    product: Product = Product(
        code=net_dict["id"],
        name=net_dict["description"])
    portico_prod: models.aton.nodes.network.PPNet = models.aton.nodes.network.PPNet(net_id= net_dict["id"])
    product.set_portico_source(portico_prod)
    networks: list[PPNetDict] = net_dict["children"]
    # log.info(f"Product {product.code}, it has {len(networks)} networks")
    for network in networks:
        net: Network = Network(
            code=network["id"],
            name=network["description"]
        )
        get_net_attributes(network, net)
        log.info(f"Is this a vendor network: {net.isVendorNetwork}")
        log.info(f"Is this a health network: {net.isHNETNetwork}")
        portico_net: models.aton.nodes.network.PPNet = models.aton.nodes.network.PPNet(net_id=network["id"])
        net.set_portico_source(portico_net)
        product.add_network(net)
    return product