import logging
from functools import singledispatch

from models.aton.nodes.organization import Organization
from models.aton.nodes.product import Product
from models.portico import PPProv, PPNet

log = logging.getLogger(__name__)

def transformer(portico_entity_list) -> list | None:
    """
    Transforms a list of portico entities into a list of organizations or products. The
    function iterates over the given input and determines whether each portico entity
    is an organization or a product. Based on the type, it transforms the entity and
    appends it to the corresponding list. The function returns the list of organizations, or the list of products. Returns
    None if neither organizations nor products are found.

    :param portico_entity_list: List of portico entities to be transformed
    :type portico_entity_list: list
    :return: List of transformed organizations or products, or None if the input list
        does not contain any valid entities
    :rtype: list | None
    """
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