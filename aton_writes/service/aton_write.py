from neomodel import db

from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_product import create_product
from aton_writes.service.upsert_organization import create_organization

import logging

from models.aton.nodes.product import Product

log = logging.getLogger(__name__)


@db.transaction
def write_to_aton(organizations: list[Organization]):
    for organization in organizations:
        create_organization(organization)


def write_products_networks(product: Product):
    create_product(product)