from models.aton.nodes.location import Location
from models.portico import PPProvTinLoc
from utils.hash_util import hash_utility


def get_hash_key_for_location(location: Location) -> str:
    return hash_utility(location.street_address,
                        location.secondary_address,
                        location.city,
                        location.state,
                        location.zip_code,
                        location.county,
                        location.county_fips)

def get_hash_key_for_prov_tin_loc(prov_tin_loc: PPProvTinLoc) -> str:
    return hash_utility(prov_tin_loc.address.addr1,
                                 prov_tin_loc.address.addr2,
                                 prov_tin_loc.address.city.ds,
                                 prov_tin_loc.address.state,
                                 prov_tin_loc.address.zip,
                                 prov_tin_loc.address.county.ds,
                                 prov_tin_loc.address.fips)