import models
from models.aton.nodes.location import Location
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_network import AssociatedRL, RoleNetwork
from models.portico import PPProvTinLoc
from utils.address_util import get_state
import logging

from models.aton.nodes.validation import Validation
from utils.location_util import get_hash_key_for_location, get_hash_key_for_prov_tin_loc

log = logging.getLogger(__name__)


def set_location(hash_code, prov_tin_loc) -> Location:
    """
    Sets the location details for a given hash code and provider location information
    and initializes a Location object with the specified attributes.

    :param hash_code: A unique string identifier used for address validation.
        This is used as the validation key while setting the pending validation
        for the created `Location` object.
    :type hash_code: str
    :param prov_tin_loc: A provider location object containing the details
        of the location such as name, address, city, state, ZIP code, county,
        FIPS code, latitude, and longitude.
    :type prov_tin_loc: ProviderLocation
    :return: A `Location` object populated with the details from the given
        `prov_tin_loc` and validated using the `hash_code`.
    :rtype: Location
    """
    location: Location = Location()
    log.debug(f"Location name:{prov_tin_loc.name}")
    portico_location: models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC = models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC(loc_id=str(prov_tin_loc.id))
    location.set_portico_source(portico_location)
    location.name = prov_tin_loc.name
    location.street_address = prov_tin_loc.address.addr1
    location.secondary_address = prov_tin_loc.address.addr2
    location.city = prov_tin_loc.address.city.ds
    if prov_tin_loc.address.county_fips:
        location.state = get_state(prov_tin_loc.address.county_fips)
    else:
        location.state = "COUNTY NOT AVAILABLE"
    location.zip_code = prov_tin_loc.address.zip
    location.county = prov_tin_loc.address.county.ds
    location.county_fips = prov_tin_loc.address.county_fips
    location.latitude = prov_tin_loc.address.latitude
    location.longitude = prov_tin_loc.address.longitude
    # ------------------------------------------------------------------------------
    # Set pending validation for the location
    # ------------------------------------------------------------------------------
    validation: Validation = Validation(type="address", source="smartystreets", validation_key=hash_code)
    location.set_pending_validation(validation)
    return location

def get_assoc_rl(pp_prov_tin_loc:PPProvTinLoc,
           role_network: RoleNetwork,
           role_instance:RoleInstance) -> tuple[AssociatedRL, bool]:
    """
    Determines the associated role location (RL) for a given provider location and role network. If the
    associated role location is not found in the role network, it checks the role instance and retrieves
    the information if present.

    This function generates a hash key for the provided provider-tin-location (PPProvTinLoc) object and
    uses it to look up the associated role location in the given role network. If the hash code does not
    correspond to any location within the role network, an additional lookup is performed in the role instance
    to retrieve the associated role location, if available.

    Logs are added for reference, including the provider's location address and the generated hash key.

    :param pp_prov_tin_loc: Object representing the provider tin location.
    :param role_network: The role network where the associated role location is expected to exist.
    :param role_instance: The role instance for secondary lookup if the role location is absent
        in the role network.
    :return: A tuple.
    """
    log.debug(f"Location Address:{pp_prov_tin_loc.address}")
    prov_tin_loc_hash_code = get_hash_key_for_prov_tin_loc(prov_tin_loc=pp_prov_tin_loc)
    log.debug(f"Hash Code:{prov_tin_loc_hash_code}")
    assoc_rl: AssociatedRL = get_assoc_loc_rn(prov_tin_loc_hash_code, role_network)
    if not assoc_rl:
        # If the role location is not present in the role network, then get it from the role instance
        assoc_rl = get_assoc_loc_ri(prov_tin_loc_hash_code, role_instance)
        return assoc_rl, False
    else:
        # If the associated role location is present in the role network, then return it
        return assoc_rl, True

def get_rn(code: str, role_instance: RoleInstance):
    """
    Retrieves a RoleNetwork instance from the given role instance that matches
    the specified network code. The function iterates through the pending
    RoleNetwork instances associated with the role instance and checks if any
    of them has a network with the specified code. If a match is found, that
    RoleNetwork instance is returned. If no match is found, the function
    returns None.

    :param code: The unique code of the network to search for.
    :type code: str
    :param role_instance: The RoleInstance object containing pending
        RoleNetwork instances.
    :type role_instance: RoleInstance
    :return: A RoleNetwork instance if a match is found; otherwise, None.
    :rtype: RoleNetwork or None
    """
    rns: list[RoleNetwork] = role_instance.get_pending_rns()
    for rn in rns:
        if rn.get_network().code == code:
            return rn
    return None

def get_assoc_loc_rn(prov_tin_loc_hash_code:str, role_network:RoleNetwork) -> AssociatedRL | None:
    """
    Searches through the pending associated role locations in the given role network and
    returns the associated role location whose location matches the provided hashed
    location code. If no match is found, it returns None.

    :param prov_tin_loc_hash_code: The hashed location code to match against
    :param role_network: The RoleNetwork instance containing associations and pending
        role locations
    :return: The matching AssociatedRL instance if found, otherwise None
    """
    for assoc_rl in role_network.get_pending_assoc_rls():
        rl = assoc_rl.role_location
        location_hash_code = get_hash_key_for_location(rl.get_location())
        if location_hash_code == prov_tin_loc_hash_code:
            return assoc_rl
    return None

def get_assoc_loc_ri(prov_tin_loc_hash_code:str, role_instance: RoleInstance) -> AssociatedRL | None:
    """
    This function attempts to find an associated role-location relationship (AssociatedRL)
    based on the provided location hash code and the role instance. It iterates through the
    pending role-location relationships of the input `role_instance` and compares their hash
    keys to the given hash code. If a match is found, it constructs an `AssociatedRL` object
    and returns it. If no match exists, the function returns None.

    :param prov_tin_loc_hash_code: The hash code representation of the provider's TIN-specific
        location for which an associated role-location relationship is searched.
    :type prov_tin_loc_hash_code: str
    :param role_instance: Instance of the RoleInstance class, representing the instance that
        contains pending role-location relationships.
    :type role_instance: RoleInstance
    :return: An `AssociatedRL` instance if a matching role-location is found; otherwise, None.
    :rtype: AssociatedRL | None
    """
    for rl in role_instance.get_pending_rls():
        location_hash_code = get_hash_key_for_location(rl.get_location())
        if location_hash_code == prov_tin_loc_hash_code:
            assoc_rl = AssociatedRL(role_location=rl)
            return assoc_rl
    return None