
from neomodel import DoesNotExist

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.pp_net import PP_NET
from models.aton.nodes.product import Product

import logging

log = logging.getLogger(__name__)


def find_product_by_code(code: str):
    try:
        return Product.nodes.get(code=code)
    except DoesNotExist:
        pass

    try:
        return PP_NET.nodes.get(net_id=code).sources.single()
    except DoesNotExist:
        return None

def find_product_by_code_or_name(code: str, name: str) -> tuple[Product | None, bool]:
    is_product_found_by_name = False
    try:
        return Product.nodes.get(code=code), is_product_found_by_name
    except DoesNotExist:
        log.debug(f"Product {code} not found by code")
        pass
    try:
        product = Product.nodes.get(name=name)
        is_product_found_by_name = True
        return product, True
    except DoesNotExist:
        log.debug(f"Product {code} with name {name} not found by name")
        return None, is_product_found_by_name

def find_pp_net_by_id(code: str):
    try:
        return LegacySystemID.nodes.get(value=code, systemIdType="NET ID", system="PORTICO")
    except DoesNotExist:
        return None