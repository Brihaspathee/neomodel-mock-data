from models.aton.nodes.location import Location
from models.portico import PPProvTinLoc
from utils.hash_util import hash_utility
from utils.address_util import get_state


def get_hash_key_for_location(location: Location) -> str:
    return hash_utility(location.street_address,
                        location.secondary_address,
                        location.city,
                        location.state,
                        location.zip_code,
                        location.county,
                        location.county_fips)

def get_hash_key_for_prov_tin_loc(prov_tin_loc: PPProvTinLoc) -> str:
    state_code = ""
    if prov_tin_loc.address.county_fips:
        state_code = get_state(prov_tin_loc.address.county_fips)
    return hash_utility(prov_tin_loc.address.addr1,
                                 prov_tin_loc.address.addr2,
                                 prov_tin_loc.address.city.ds,
                                 state_code,
                                 prov_tin_loc.address.zip,
                                 prov_tin_loc.address.county.ds,
                                 prov_tin_loc.address.county_fips)