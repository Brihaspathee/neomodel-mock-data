from config import settings, attribute_settings, contact_settings, county_settings
from db import PorticoDB, init_db
from models.aton.nodes.organization import Organization
from models.aton.nodes.product import Product
from portico_reads.service.provider import provider_read
from portico_reads.service.network import network_read
import portico_reads.service.fmg_codes.load_fmg_codes as fmg_codes
from transform.transformers import transformer
from utils.log_provider import log_providers, log_provider
from aton_writes.service.aton_write import write_to_aton, write_products_networks
from transform import transform_network
from transform import transform_provider
import logging

from models.portico import PPNet, PPProv

log = logging.getLogger(__name__)

def main():
    log.debug("Starting...")
    log.debug(f"Running on {settings.ENVIRONMENT} environment")
    log.debug(f"POSTGRES info {settings.POSTGRES} environment")
    log.debug(f"NEO4J info {settings.NEO4J} environment")
    log.debug(f"ATTRIBUTES CONFIG {attribute_settings.ATTRIBUTES_CONFIG}")
    log.debug(f"Contact use mapping:{contact_settings.CONTACT_USE_MAPPING}")
    log.debug(f"Address use mapping:{contact_settings.ADDRESS_USE_MAPPING}")
    log.debug(f"County state mapping:{county_settings.COUNTY_STATE_MAPPING}")
    logging.basicConfig(level=logging.DEBUG)

    # Read the providers from Portico
    portico_db: PorticoDB = PorticoDB()
    portico_db.connect()
    init_db()

    user_input: str = input("Select an option: \n1. Load all data\n2. Load data for a single provider :")
    if user_input == "1":
        log.debug("Loading all data")
        with (portico_db.get_session() as session):
            fmg_codes.load_fmg_codes(session)
            # log.debug(f"FMG_CODES: {fmg_codes.FMG_CODES}")
            pp_nets: list[PPNet] = network_read.get_networks(session)
            providers: list[PPProv] = provider_read.read_provider(session)
            # log_providers(providers)
            products: list[Product] = transformer(pp_nets)
            for product in products:
                write_products_networks(product)
            organizations: list[Organization]=transformer(providers)
            # for org in organizations:
            #     log.info(f"Organization: {org}")
            #     for practitioner in org.get_pending_practitioners():
            #         log.info(f"Practitioner: {practitioner}")
            #         log.info(f"Practitioner Role Instance:{practitioner.get_pending_role_instance()}")
            write_to_aton(organizations)
    elif user_input == "2":
        log.debug("Loading data for a single provider")
        with (portico_db.get_session() as session):
            provider: PPProv = provider_read.get_provider_attributes(session, 1)
            orgs = transformer(list([provider]))
            for org in orgs:
                log.debug(f"Org:{org.name}")
            write_to_aton(orgs)



if __name__ == "__main__":
    # driver = get_driver()
    main()
    # close_driver()