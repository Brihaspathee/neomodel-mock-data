import logging

from models.aton.nodes.pp_net import PPNet
from models.aton.nodes.product import Product
from repository.product_repo import find_product_by_code_or_name, find_pp_net_by_id
from repository.network_repo import find_network_by_code_or_name

log = logging.getLogger(__name__)

def create_product(product: Product):
    try:
        product = find_or_create_product(product)
        for network in product.get_pending_networks():
            network = find_or_create_network(network)
            # log.debug(f"Product {product.code} is connected to {network.name}")
            network.product.connect(product)
        return product
    except Exception as e:
        log.error(f"Error writing product {product.code} to Aton: {e}")
        # log.error("Unable to create product due to {}".format(e))
        return None


def find_or_create_product(product):
    existing_product, is_prod_found_by_name = find_product_by_code_or_name(product.code, product.name)
    if not existing_product:
        product.save()
        pp_net: PPNet = product.get_portico_source()
        pp_net.save()
        pp_net.aton_prod.connect(product)
        log.error(f"Created product {product.name}, it has {len(product.get_pending_networks())} networks")
        return product
    else:
        # The product already exists with the same id and/or name
        log.debug(f"Product {product.code} already exists")
        if is_prod_found_by_name:
            # This means the product node was found using the name of the product
            # so the portico had two products with the same name but different ids.
            # In ATON we will not be creating two nodes with the same name.
            # One ATON Product node will be linked to more than one PP_NET nodes
            # that have the same name but different ids.
            # Before creating the PP_NET node, we need to check if the PP_NET node already exists.
            # If it does not, then create it.
            pp_net: PPNet = find_pp_net_by_id(product.get_portico_source().net_id)
            if pp_net is None:
                pp_net: PPNet = product.get_portico_source()
                log.debug(f"Product {product.code}'s portico source is: {pp_net}")
                pp_net.save()
                pp_net.aton_prod.connect(existing_product)
        product = existing_product
    return product

def find_or_create_network(network):
    existing_network, is_net_found_by_name = find_network_by_code_or_name(network.code, network.name)
    if not existing_network:
        network.save()
        pp_net: PPNet = network.get_portico_source()
        pp_net.save()
        pp_net.aton_net.connect(network)
        log.debug(f"Created network  {network.name}")
    else:
        # The network already exists with the same id and/or name
        log.debug(f"Network {network.name} already exists")
        if is_net_found_by_name:
            # This means the network node was found using the name of the network
            # so the portico had two networks with the same name but different ids.
            # In ATON we will not be creating two nodes with the same name.
            # One ATON Network node will be linked to more than one PP_NET nodes
            # that have the same name but different ids
            pp_net: PPNet = find_pp_net_by_id(network.get_portico_source().net_id)
            if pp_net is None:
                pp_net: PPNet = network.get_portico_source()
                log.debug(f"Network {network.code}'s portico source is: {pp_net}")
                pp_net.save()
                pp_net.aton_net.connect(existing_network)
        network = existing_network
    return network