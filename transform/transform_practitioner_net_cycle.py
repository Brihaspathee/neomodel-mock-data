import logging

from models.aton.context.role_network_context import RoleNetworkContext
from models.aton.nodes.network import Network
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_network import RoleNetwork
from models.aton.relationships.role_location_serves import RoleLocationServes
from models.portico import PPPracNetCycle, PPProv
from repository import network_repo
from transform.transform_utils import get_rn, get_assoc_rl

log = logging.getLogger(__name__)


def transform_practitioner_net_cycle(prac_net_cycles: list[PPPracNetCycle], role_instance: RoleInstance, prov_id:int):

    for prac_net_cycle in prac_net_cycles:
        role_network: RoleNetwork | None = None
        log.debug(f"Network Address:{prac_net_cycle.net_id}")
        # ------------------------------------------------------------------------------
        # Check if the network already is present in the pending role network list present in role instance
        # If yes, then use that to update the locations, because in Portico a single practitioner network cycle
        # can have multiple network cycles, to avoid creating a RoleNetwork for the same network,
        # we first check if the network is already present in the role instance.
        # ------------------------------------------------------------------------------
        rn: RoleNetwork = get_rn(code=str(prac_net_cycle.net_id), role_instance=role_instance)
        is_rn_present: bool = True if rn else False
        if is_rn_present:
            # If it is already present, then use that to update the locations
            role_network = rn
        else:
            # If not present, then create a new role network
            role_network = RoleNetwork()
            role_network.context = RoleNetworkContext(role_network)
            role_network.suppress_pcp_assignment = False
            # ------------------------------------------------------------------------------
            # The network associated with the practitioner should already be available in
            # ATON. If it is not present then raise error.
            # ------------------------------------------------------------------------------
            network: Network = network_repo.find_network_by_code(code=str(prac_net_cycle.net_id))
            if not network:
                log.error(f"Network not found in Aton: {prac_net_cycle.net_id}")
                raise RuntimeError(f"Network not found in Aton: {prac_net_cycle.net_id}")
            log.debug(f"Network found its element id is :{network.element_id}")
            # ------------------------------------------------------------------------------
            # Set the network in the role network so that it can be associated
            # ------------------------------------------------------------------------------
            role_network.context.set_network(network)
        # ------------------------------------------------------------------------------
        # Iterate through the location cycles within the provider network cycle
        # ------------------------------------------------------------------------------
        for loc_cycle in prac_net_cycle.loc_cycles:
            # ------------------------------------------------------------------------------
            # Get the provider from the location cycle and process only for the provider
            # for whom the transformation is being applied.
            # ------------------------------------------------------------------------------
            provider: PPProv = loc_cycle.provider
            if provider.id == prov_id:
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
                    role_network.context.add_assoc_rl(assoc_rl)
        if not is_rn_present:
            # If the role network is not present in the role instance, then add it to the list
            role_instance.context.add_rn(role_network)
    log.debug(f"# of Role Networks: {len(role_instance.context.get_rns())}")
