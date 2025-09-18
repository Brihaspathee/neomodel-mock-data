import logging

from models.aton.nodes.pp_net import PPNet
from models.aton.nodes.product import Product
from repository.product_repo import find_product_by_code_or_name
from repository.network_repo import find_network_by_code_or_name

log = logging.getLogger(__name__)

def create_product(product: Product):
    try:
        product = find_or_create_product(product)
        log.info(f"Created product {product.name}, it has {len(product.get_pending_networks())} networks")
        for network in product.get_pending_networks():
            network = find_or_create_network(network)
            # log.info(f"Product {product.code} is connected to {network.name}")
            network.product.connect(product)
        return product
    except Exception as e:
        log.error("Unable to create product due to {}".format(e))
        return None


def find_or_create_product(product):
    existing_product, is_prod_found_by_name = find_product_by_code_or_name(product.code, product.name)
    if not existing_product:
        product.save()
        pp_net: PPNet = product.get_portico_source()
        pp_net.save()
        pp_net.aton_net_prod.connect(product)
        log.info(f"Created product {product.name}, it has {len(product.get_pending_networks())} networks")
    else:
        # The product already exists with the same id and/or name
        product = existing_product
        if is_prod_found_by_name:
            # This means the product node was found using the name of the product
            # so the portico had two products with the same name but different ids.
            # In ATON we will not be creating two nodes with the same name.
            # One ATON Product node will be linked to more than one PP_NET nodes
            # that have the same name but different ids
            pp_net: PPNet = product.get_portico_source()
            pp_net.save()
            pp_net.aton_net_prod.connect(existing_product)
    return product

def find_or_create_network(network):
    existing_network, is_net_found_by_name = find_network_by_code_or_name(network.code, network.name)
    if not existing_network:
        network.save()
        pp_net: PPNet = network.get_portico_source()
        pp_net.save()
        pp_net.aton_net_prod.connect(network)
        log.info(f"Created network  {network.name}")
    else:
        # The network already exists with the same id and/or name
        network = existing_network
        if is_net_found_by_name:
            # This means the network node was found using the name of the network
            # so the portico had two networks with the same name but different ids.
            # In ATON we will not be creating two nodes with the same name.
            # One ATON Network node will be linked to more than one PP_NET nodes
            # that have the same name but different ids
            pp_net: PPNet = network.get_portico_source()
            pp_net.save()
            pp_net.aton_net_prod.connect(existing_network)
    return network