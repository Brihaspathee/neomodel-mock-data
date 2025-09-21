from models.portico.pp_prov import PPProv
import logging

log = logging.getLogger(__name__)


def log_providers(providers: list[PPProv]):
    for provider in providers:
        log_provider(provider)

def log_provider(provider: PPProv):
    log.info(provider)
    log.info(provider.name)
    log.info(provider.prov_type.type_ds)
    log.info(provider.tin.tin)
    for address in provider.addresses:
        log.info(address)
        log.info(address.address.type)
        log.info(address.address.addr1)
        log.info(address.address.city.ds)
        log.info(address.address.county.ds)
        for phone in address.address.phones:
            log.info(phone)
            log.info(phone.phone.type)
            log.info(phone.phone.num)
    for attribute in provider.attributes:
        log.info(f"Provider Attribute:{attribute.attribute_type}")
        log.info(attribute)
        log.info(attribute.attribute_type)
        for value in attribute.values:
            log.info(value)
            log.info(value.field)
            log.info(value.value)
            log.info(value.value_date)
    for prov_loc in provider.prov_locs:
        log.info(f"Locations associated with the Provider - {prov_loc.location}")
    for prov_loc_attr in provider.loc_attributes:
        log.info(f"Location Attributes associated with the Provider - {prov_loc_attr.location}")
        log.info(f"Location Attribute type id - {prov_loc_attr.attribute_id}")
        for value in prov_loc_attr.values:
            log.info(f"Location Attribute Value - {value}")
            log.info(f"Location Attribute Value Field - {value.field}")
    for network in provider.networks:
        log.info(f"Network cycle id - {network.id}")
        log.info(f"Network in the cycle - {network.network}")
        for loc_cycle in network.loc_cycles:
            log.info(f"Network location cycle {loc_cycle}")
            log.info(f"Location in the cycle - {loc_cycle.location}")