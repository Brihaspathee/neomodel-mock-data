from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_network import RoleNetwork, AssociatedRL
from models.aton.nodes.network import Network
from models.aton.relationships.role_location_serves import RoleLocationServes
from models.portico import PPProvNetCycle, PPProvTinLoc
from transform.transform_utils import get_assoc_rl, get_rn
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
        log.debug(f"Network Address:{prov_net_cycle.net_id}")
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
            log.debug(f"Network found its element id is :{network.element_id}")
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
    log.debug(f"# of Role Networks: {len(role_instance.get_pending_rns())}")

