import logging

from config.county_settings import COUNTY_STATE_MAPPING
from models.aton.nodes.address import Address
from models.portico import PPAddr

log = logging.getLogger(__name__)


def portico_address_to_aton(pp_addr: PPAddr) -> Address:
    address: Address = Address()
    address.streetAddress = pp_addr.addr1
    address.secondaryAddress = pp_addr.addr2
    address.city = pp_addr.city.ds
    address.zip_code = pp_addr.zip
    address.county = pp_addr.county.ds
    address.county_fips = pp_addr.county_fips
    if pp_addr.county_fips:
        address.state = get_state(pp_addr.county_fips)
    else:
        address.state = "COUNTY NOT AVAILABLE"
    address.latitude = pp_addr.latitude
    address.longitude = pp_addr.longitude
    return address

def get_state(county_fips: str) -> str:
    log.debug(f"Count fips: {county_fips}")
    state_number =  county_fips[:2]
    log.debug(f"State number: {state_number}")
    state_code = COUNTY_STATE_MAPPING.get(state_number).get("code")
    log.debug(f"State code: {state_code}")
    return state_code