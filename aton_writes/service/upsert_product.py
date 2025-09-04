import logging

from models.aton.product import Product

log = logging.getLogger(__name__)

def create_product(product: Product):
    try:
        product.save()
        log.info(f"Created product {product.name}, it has {len(product.get_pending_networks())} networks")
        for network in product.get_pending_networks():
            network.save()
            # log.info(f"Product {product.code} is connected to {network.name}")
            network.product.connect(product)
        return product
    except Exception as e:
        log.error("Unable to create product due to {}".format(e))
        return None