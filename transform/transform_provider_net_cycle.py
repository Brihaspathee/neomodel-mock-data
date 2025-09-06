from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork, AssociatedRL
from models.aton.nodes.network import Network
from models.aton.relationships.role_location_serves import RoleLocationServes
from models.portico import PPProvNetCycle, PPProvTinLoc
from utils.location_util import get_hash_key_for_prov_tin_loc, get_hash_key_for_location
from repository.network_repo import find_network_by_code
import logging

from repository import network_repo

log = logging.getLogger(__name__)


def transform_provider_net_cycle(prov_net_cycles: list[PPProvNetCycle], role_instance: RoleInstance):
    """
    Transforms and maps provider network cycles to pending role networks within the given role instance.

    Iterates through a list of provider network cycles, checks the existence of the corresponding role
    network within the role instance, and creates or updates the role network. For each location cycle
    within the provider network cycle, it retrieves or associates the related role location, updating its
    service edges and associating pending configurations within the role network and instance, if necessary.

    :param prov_net_cycles: A list of provider network cycles containing network and location cycle
                            information to be transformed.
    :type prov_net_cycles: list[PPProvNetCycle]
    :param role_instance: The role instance to which the transformed role networks and associated locations
                          are added as pending entries.
    :type role_instance: RoleInstance
    :return: None
    :rtype: None
    """
    for prov_net_cycle in prov_net_cycles:
        role_network: RoleNetwork | None = None
        log.info(f"Network Address:{prov_net_cycle.net_id}")
        # ------------------------------------------------------------------------------
        # Check if the network already is present in the pending role network list present in role instance
        # If yes, then use that to update the locations, because in Portico a single provider network cycle
        # can have multiple network cycles, to avoid creating a RoleNetwork for the same network,
        # we first check if the network is already present in the role instance.
        # ------------------------------------------------------------------------------
        rn: RoleNetwork = get_rn(code=str(prov_net_cycle.net_id), role_instance=role_instance)
        is_rn_present: bool = True if rn else False
        if is_rn_present:
            # If it is already present, then use that to update the locations
            role_network = rn
        else:
            # If not present, then create a new role network
            role_network = RoleNetwork()
            role_network.suppress_pcp_assignment = False
            # ------------------------------------------------------------------------------
            # The network associated with the provider should already be available in
            # ATON. If it is not present then raise error.
            # ------------------------------------------------------------------------------
            network: Network = network_repo.find_network_by_code(code=str(prov_net_cycle.net_id))
            if not network:
                log.error(f"Network not found in Aton: {prov_net_cycle.net_id}")
                raise RuntimeError(f"Network not found in Aton: {prov_net_cycle.net_id}")
            log.info(f"Network found its element id is :{network.element_id}")
            # ------------------------------------------------------------------------------
            # Set the network in the role network so that it can be associated
            # ------------------------------------------------------------------------------
            role_network.set_network(network)
        # ------------------------------------------------------------------------------
        # Iterate through the location cycles within the provider network cycle
        # ------------------------------------------------------------------------------
        for loc_cycle in prov_net_cycle.loc_cycles:
            # ------------------------------------------------------------------------------
            # See of the role location is already present in the role network
            # In a prior iteration if the RoleLocation was retrieved from the role instance and processed,
            # then that very same role location should be used to append the role location serves edges
            # If it is not present in the role network, then get it from the role instance.
            # ------------------------------------------------------------------------------
            assoc_rl,present_in_rn = get_assoc_rl(loc_cycle.location, role_network, role_instance)
            rls: RoleLocationServes = RoleLocationServes()
            rls.start_date = loc_cycle.start_date
            rls.end_date = loc_cycle.end_date
            assoc_rl.rls_edges.append(rls)
            if not present_in_rn:
                # If the role location is not present in the role network, then add it to the list
                role_network.add_pending_assoc_rl(assoc_rl)
        if not is_rn_present:
            # If the role network is not present in the role instance, then add it to the list
            role_instance.add_pending_rn(role_network)
    log.info(f"# of Role Networks: {len(role_instance.get_pending_rns())}")


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
    log.info(f"Location Address:{pp_prov_tin_loc.address}")
    prov_tin_loc_hash_code = get_hash_key_for_prov_tin_loc(prov_tin_loc=pp_prov_tin_loc)
    log.info(f"Hash Code:{prov_tin_loc_hash_code}")
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

