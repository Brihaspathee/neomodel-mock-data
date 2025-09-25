from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.portico import PPPrac, PPProv, PPProvTinLoc
from transform.transform_practitioner_net_cycle import transform_practitioner_net_cycle
from utils.location_util import get_hash_key_for_prov_tin_loc
from transform.transform_utils import set_location
import logging

log = logging.getLogger(__name__)

def transform_practitioner_location(pp_prac:PPPrac, role_instance:RoleInstance, prov_id:int):
    for prac_loc in pp_prac.locations:
        pp_prov: PPProv = prac_loc.provider
        # Check if the provider ID matches with the provider
        # for whom the transformation is being applied.
        if pp_prov.id == prov_id:
            role_location: RoleLocation = RoleLocation()
            if prac_loc.PRIMARY == "Y":
                role_location.set_is_primary(True)
            pp_prov_tin_loc: PPProvTinLoc = prac_loc.location
            hash_code = get_hash_key_for_prov_tin_loc(prov_tin_loc=pp_prov_tin_loc)
            location = set_location(hash_code, pp_prov_tin_loc)
            role_location.set_location(location)
            role_instance.add_pending_rl(role_location)
    log.info(f"Provider Id:{prov_id}")
    log.info(f"Added {len(role_instance.get_pending_rls())} role locations to role instance")
    if pp_prac.networks:
        transform_practitioner_net_cycle(prac_net_cycles=pp_prac.networks, role_instance=role_instance, prov_id=prov_id)