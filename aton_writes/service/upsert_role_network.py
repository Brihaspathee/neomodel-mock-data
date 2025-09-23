from models.aton.nodes.network import Network
from models.aton.nodes.role_instance import RoleInstance
import logging

log = logging.getLogger(__name__)


def process_role_networks(role_instance:RoleInstance):
    for rn in role_instance.get_pending_rns():
        rn.save()
        network: Network = rn.get_network()
        rn.network.connect(network)
        role_instance.role_networks.connect(rn)
        for assoc_rl in rn.get_pending_assoc_rls():
            rl = assoc_rl.role_location
            log.debug(f"Role Location inside the network:{rl.element_id}")
            for rls in assoc_rl.rls_edges:
                rl.role_network.connect(rn, {
                    "start_date": rls.start_date,
                    "end_date": rls.end_date
                })