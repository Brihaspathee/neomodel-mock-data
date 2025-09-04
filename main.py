from config import settings
from db import PorticoDB, init_db
from models.aton.organization import Organization
from models.aton.product import Product
from portico_reads.service.provider import provider_read
from portico_reads.service.network import network_read
from utils.log_provider import log_providers
from transform.transformers import transformer
import transform.transform_network
import transform.transform_provider
from aton_writes.service.aton_write import write_to_aton, write_products_networks
import logging

from models.portico import PPNet, PPProv

log = logging.getLogger(__name__)

def main():
    log.info("Starting...")
    log.info(f"Running on {settings.ENVIRONMENT} environment")
    log.info(f"POSTGRES info {settings.POSTGRES} environment")
    log.info(f"NEO4J info {settings.NEO4J} environment")
    log.info(f"Attributes JSON{settings.FLAT_CONFIG}")
    logging.basicConfig(level=logging.DEBUG)

    # Read the providers from Portico
    portico_db: PorticoDB = PorticoDB()
    portico_db.connect()
    init_db()

    with (portico_db.get_session() as session):
        pp_nets: list[PPNet] = network_read.get_networks(session)
        providers: list[PPProv] = provider_read.read_provider(session)
    # log_providers(providers)
    for pp_net in pp_nets:
        pp_net_dict = pp_net.to_dict()
        log.info(f"PP net {pp_net_dict}")
    products: list[Product] = transformer(pp_nets)
    for product in products:
        write_products_networks(product)
    organizations: list[Organization]=transformer(providers)
    for organization in organizations:
        write_to_aton(organization)




if __name__ == "__main__":
    # driver = get_driver()
    main()
    # close_driver()