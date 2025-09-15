from models.aton.nodes.address import Address
from models.portico import PPAddr


def portico_address_to_aton(pp_addr: PPAddr) -> Address:
    address: Address = Address()
    address.streetAddress = pp_addr.addr1
    address.secondaryAddress = pp_addr.addr2
    address.city = pp_addr.city.ds
    address.state = pp_addr.state
    address.zip_code = pp_addr.zip
    address.county = pp_addr.county.ds
    address.county_fips = pp_addr.fips
    address.latitude = pp_addr.latitude
    address.longitude = pp_addr.longitude
    return address