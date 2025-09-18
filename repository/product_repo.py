from imaplib import Flags

from neomodel import DoesNotExist
from models.aton.nodes.pp_net import PPNet
from models.aton.nodes.product import Product


def find_product_by_code(code: str):
    try:
        return Product.nodes.get(code=code)
    except DoesNotExist:
        pass

    try:
        return PPNet.nodes.get(net_id=code).sources.single()
    except DoesNotExist:
        return None

def find_product_by_code_or_name(code: str, name: str) -> tuple[Product | None, bool]:
    is_product_found_by_name = False
    try:
        return Product.nodes.get(code=code), is_product_found_by_name
    except DoesNotExist:
        pass
    try:
        product = Product.nodes.get(name=name)
        is_product_found_by_name = True
        return product, True
    except DoesNotExist:
        return None, is_product_found_by_name