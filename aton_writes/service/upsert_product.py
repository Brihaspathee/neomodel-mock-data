import logging

from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.product import Product
from repository.product_repo import find_product_by_code_or_name, find_pp_net_by_id
from repository.network_repo import find_network_by_code_or_name

log = logging.getLogger(__name__)


def create_product(product: Product):
    """
    Creates or retrieves a product and establishes connections with its pending networks.

    The function first attempts to find an existing product or create a new one if it does
    not already exist. After ensuring the product is created, it processes its pending
    networks by either finding or creating each network. For each network associated with
    the product, the necessary connection between the product and the network is established.
    If the operation fails at any point, an error is logged and the function returns None.

    :param product: The product to be created or retrieved and connected to its pending networks.
    :type product: Product
    :return: The created or retrieved product with established network connections, or None if an error occurs.
    :rtype: Product or None
    """
    try:
        product = find_or_create_product(product)
        for network in product.context.get_networks():
            network = find_or_create_network(network)
            # log.debug(f"Product {product.code} is connected to {network.name}")
            network.product.connect(product)
        return product
    except Exception as e:
        log.error(f"Error writing product {product.code} to Aton: {e}")
        # log.error("Unable to create product due to {}".format(e))
        return None


def find_or_create_product(product):
    """
    Finds an existing product by its code or name, or creates a new one if it does not exist.
    This function handles relationships between the product and its associated legacy
    system identification (PP_NET). If the product is created or found by name and there
    are potential pre-existing associations (PP_NET), those are resolved and linked
    appropriately.

    The function logs detailed information about the actions, such as creating a new product,
    associating legacy system IDs, or determining that a product already exists.

    :param product: The product instance to locate or create.
    :type product: Product
    :return: The existing or newly created product.
    :rtype: Product
    """
    existing_product, is_prod_found_by_name = find_product_by_code_or_name(product.code, product.name)
    if not existing_product:
        product.save()
        pp_net: LegacySystemIdentifier = product.context.get_portico_source()
        pp_net.save()
        log.debug(f"Product node and PP_NET node created for {product.code}")
        pp_net.product.connect(product)
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
            pp_net: LegacySystemIdentifier = find_pp_net_by_id(product.context.get_portico_source().value)
            if pp_net is None:
                pp_net: LegacySystemIdentifier = product.context.get_portico_source()
                log.debug(f"Product {product.code}'s portico source is: {pp_net}")
                pp_net.save()
                log.debug(f"PP_NET node created for product {product.code}")
                pp_net.product.connect(existing_product)
        existing_product.context = product.context
        product = existing_product
    return product


def find_or_create_network(network):
    """
    Finds an existing network by its code or name or creates a new network if one does not already exist.

    If the network already exists and is found using its name, it ensures that the portico
    source for this network is connected to the existing network, avoiding the creation of
    multiple nodes with the same name in ATON. If a network node does not exist, a new one
    will be created along with its corresponding portico source, ensuring proper linkage
    between the network and its portico representation.

    :param network: The network object to be checked against existing networks or created
        if a matching network does not already exist.
    :type network: Network
    :return: A reference to the existing or newly created network.
    :rtype: Network
    """
    existing_network, is_net_found_by_name = find_network_by_code_or_name(network.code, network.name)
    if not existing_network:
        network.save()
        pp_net: LegacySystemIdentifier = network.context.get_portico_source()
        pp_net.save()
        pp_net.network.connect(network)
        log.debug(f"Created Network and PP_NET node for {network.code}")
    else:
        # The network already exists with the same id and/or name
        log.debug(f"Network {network.name} already exists")
        if is_net_found_by_name:
            # This means the network node was found using the name of the network
            # so the portico had two networks with the same name but different ids.
            # In ATON we will not be creating two nodes with the same name.
            # One ATON Network node will be linked to more than one PP_NET nodes
            # that have the same name but different ids
            pp_net: LegacySystemIdentifier = find_pp_net_by_id(network.context.get_portico_source().value)
            if pp_net is None:
                pp_net: LegacySystemIdentifier = network.context.get_portico_source()
                log.debug(f"Network {network.code}'s portico source is: {pp_net}")
                pp_net.save()
                log.debug(f"PP_NET node created for network {network.code}")
                pp_net.network.connect(existing_network)
        existing_network.context = network.context
        network = existing_network
    return network