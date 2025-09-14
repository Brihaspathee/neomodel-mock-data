from neomodel import db

from models.aton.nodes.organization import Organization
from aton_writes.service.upsert_product import create_product
from aton_writes.service.upsert_organization import create_organization, update_organization, upsert_organizations

import logging

from models.aton.nodes.product import Product

log = logging.getLogger(__name__)


@db.transaction
def write_to_aton(organizations: list[Organization]):
    upsert_organizations(organizations)
    # sorted_orgs = sorted(
    #     organizations,
    #     key=lambda org: (org.parent_ppg_id is not None, org.parent_ppg_id or "")
    # )
    # for organization in sorted_orgs:
    #     prov_id = organization.get_portico_source().prov_id
    #     existing_org = get_organization_by_prov_id(prov_id)
    #     if existing_org:
    #         existing_org.name = organization.name
    #         update_organization(existing_org)
    #     else:
    #         create_organization(organization)


def write_products_networks(product: Product):
    create_product(product)