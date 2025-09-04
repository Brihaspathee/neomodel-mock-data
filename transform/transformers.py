import logging
from functools import singledispatch

from models.aton.organization import Organization
from models.aton.product import Product
from models.portico import PPProv, PPNet

log = logging.getLogger(__name__)

def transformer(portico_entity_list) -> list | None:
    log.info("Transformer")
    organizations: list[Organization] = []
    products: list[Product] = []
    is_org: bool = False
    is_product: bool = False
    for porticoEntity in portico_entity_list:
        if isinstance(porticoEntity,PPProv):
            is_org = True
            organization: Organization = transform_to_aton(porticoEntity)
        elif isinstance(porticoEntity,PPNet):
            is_product = True
            product: Product = transform_to_aton(porticoEntity)
        if is_org:
            organizations.append(organization)
        if is_product:
            products.append(product)
    if organizations:
        return organizations
    elif products:
        return products
    else:
        return None

@singledispatch
def transform_to_aton(arg):
    raise TypeError(f"{arg} is not a valid Portico type")