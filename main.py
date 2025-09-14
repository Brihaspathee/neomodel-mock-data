from config import settings, attribute_settings, contact_settings
from db import PorticoDB, init_db
from models.aton.nodes.organization import Organization
from models.aton.nodes.product import Product
from portico_reads.service.provider import provider_read
from portico_reads.service.network import network_read
from transform.transformers import transformer
from utils.log_provider import log_providers, log_provider
from aton_writes.service.aton_write import write_to_aton, write_products_networks
from transform import transform_network
from transform import transform_provider
import logging

from models.portico import PPNet, PPProv

log = logging.getLogger(__name__)

def main():
    log.info("Starting...")
    log.info(f"Running on {settings.ENVIRONMENT} environment")
    log.info(f"POSTGRES info {settings.POSTGRES} environment")
    log.info(f"NEO4J info {settings.NEO4J} environment")
    log.info(f"ATTRIBUTES CONFIG {attribute_settings.ATTRIBUTES_CONFIG}")
    log.info(f"Contact use mapping:{contact_settings.CONTACT_USE_MAPPING}")
    log.info(f"Address use mapping:{contact_settings.ADDRESS_USE_MAPPING}")
    logging.basicConfig(level=logging.DEBUG)

    # Read the providers from Portico
    portico_db: PorticoDB = PorticoDB()
    portico_db.connect()
    init_db()

    user_input: str = input("Select an option: \n1. Load all data\n2. Load data for a single provider :")
    if user_input == "1":
        log.info("Loading all data")
        with (portico_db.get_session() as session):
            pp_nets: list[PPNet] = network_read.get_networks(session)
            providers: list[PPProv] = provider_read.read_provider(session)
        log_providers(providers)
        products: list[Product] = transformer(pp_nets)
        for product in products:
            write_products_networks(product)
        organizations: list[Organization]=transformer(providers)
        write_to_aton(organizations)
    elif user_input == "2":
        log.info("Loading data for a single provider")
        with (portico_db.get_session() as session):
            provider: PPProv = provider_read.get_provider_attributes(session, 1)
            orgs = transformer(list([provider]))
            for org in orgs:
                log.info(f"Org:{org.name}")
            write_to_aton(orgs)
        # for attribute in provider.attributes:
        #     log.info(f"Provider Attribute:{attribute.attribute_type}")
        #     log.info(attribute)
        #     log.info(attribute.attribute_type)
        #     for value in attribute.values:
        #         log.info(value)
        #         log.info(value.field)
        #         log.info(value.value)
        #         log.info(value.value_date)



if __name__ == "__main__":
    # driver = get_driver()
    main()
    # close_driver()