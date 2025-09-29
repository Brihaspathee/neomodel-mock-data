from models.portico import PPPrac
from models.portico.pp_prov import PPProv
import logging

log = logging.getLogger(__name__)


def log_providers(providers: list[PPProv]):
    for provider in providers:
        log_provider(provider)

def log_provider(provider: PPProv):
    log.debug(provider)
    log.debug(provider.name)
    log.debug(provider.prov_type.type_ds)
    log.debug(provider.tin.tin)
    for address in provider.addresses:
        log.debug(address)
        log.debug(address.address.type)
        log.debug(address.address.addr1)
        log.debug(address.address.city.ds)
        log.debug(address.address.county.ds)
        for phone in address.address.phones:
            log.debug(phone)
            log.debug(phone.phone.type)
            log.debug(phone.phone.num)
    for attribute in provider.attributes:
        log.debug(f"Provider Attribute:{attribute.attribute_type}")
        log.debug(attribute)
        log.debug(attribute.attribute_type)
        for value in attribute.values:
            log.debug(value)
            log.debug(value.field)
            log.debug(value.value)
            log.debug(value.value_date)
    for prov_loc in provider.prov_locs:
        log.debug(f"Locations associated with the Provider - {prov_loc.location}")
    for prov_loc_attr in provider.loc_attributes:
        log.debug(f"Location Attributes associated with the Provider - {prov_loc_attr.location}")
        log.debug(f"Location Attribute type id - {prov_loc_attr.attribute_id}")
        for value in prov_loc_attr.values:
            log.debug(f"Location Attribute Value - {value}")
            log.debug(f"Location Attribute Value Field - {value.field}")
    for prov_loc_ofhour in provider.loc_ofhours:
        log.debug(f"Location of hours associated with the Provider - {prov_loc_ofhour}")
        log.debug(f"Location with the Provider - {prov_loc_ofhour.location}")
        log.debug(f"Location event - {prov_loc_ofhour.event}")
        log.debug(f"Location day - {prov_loc_ofhour.dayofweek}")
        log.debug(f"Location Time - {prov_loc_ofhour.time}")
    for network in provider.networks:
        log.debug(f"Network cycle id - {network.id}")
        log.debug(f"Network in the cycle - {network.network}")
        for loc_cycle in network.loc_cycles:
            log.debug(f"Network location cycle {loc_cycle}")
            log.debug(f"Location in the cycle - {loc_cycle.location}")
    for prac_loc in provider.prac_locs:
        log.debug(f"Practitioner location - {prac_loc}")
        log.debug(f"Practitioner - {prac_loc.practitioner}")
        log.debug(f"Location - {prac_loc.location}")
        practitioner: PPPrac = prac_loc.practitioner
        for attribute in practitioner.attributes:
            log.info(f"Practitioner Attribute - {attribute}")
            log.info(f"Practitioner Attribute Type - {attribute.attribute_type}")
            for value in attribute.values:
                log.info(f"Practitioner Attribute Value - {value}")
                log.info(f"Practitioner Attribute Value Field - {value.field}")
        for prac_net_cycle in practitioner.networks:
            log.debug(f"Practitioner network cycle - {prac_net_cycle}")
            log.debug(f"Practitioner network - {prac_net_cycle.network}")
            for loc_cycle in prac_net_cycle.loc_cycles:
                log.debug(f"Practitioner location cycle - {loc_cycle}")
                log.debug(f"Practitioner location - {loc_cycle.location}")
