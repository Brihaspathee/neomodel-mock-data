from neomodel import db

from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_product import create_product
from aton_writes.service.upsert_organization import create_organization, update_organization, upsert_organizations

import logging

from models.aton.nodes.product import Product

log = logging.getLogger(__name__)



@db.transaction
def write_to_aton(organizations: list[Organization]):
    """
    Writes a list of organizations to the ATON system using a transactional database
    operation. This function ensures that the organizations are upserted into the
    database, either updating existing records or inserting new ones as needed.

    :param organizations: A list of Organization objects to be written to the
        ATON system.
    :type organizations: list[Organization]
    :return: None
    """
    upsert_organizations(organizations)


def write_products_networks(product: Product):
    """
    Writes the product data to the networks by invoking the appropriate
    helper functions to handle the product creation logic. This function
    is responsible for initiating the process of network communication with
    the provided product details.

    :param product: The product data object that contains all relevant details
        required for creation on the networks.
    :type product: Product

    :return: None
    """
    create_product(product)