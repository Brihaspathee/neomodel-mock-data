import models
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance
from models.portico import PPProv, PPPrac
import logging
log = logging.getLogger(__name__)

def transform_practitioner(pp_prov:PPProv, organization: Organization):
    for prac_loc in pp_prov.prac_locs:
        log.info(f"Practitioner location - {prac_loc}")
        log.info(f"Practitioner - {prac_loc.practitioner}")
        log.info(f"Location - {prac_loc.location}")
        pp_prac: PPPrac = prac_loc.practitioner
        practitioner: Practitioner = Practitioner(first_name=pp_prac.fname,
                                                  last_name=pp_prac.lname,
                                                  middle_name=pp_prac.mname,
                                                  birth_date=pp_prac.dob,
                                                  gender=pp_prac.sex,
                                                  ssn=pp_prac.ssn,
                                                  salutation=pp_prac.xname)
        role_instance: RoleInstance = RoleInstance()
        practitioner.set_pending_role_instance(role_instance)
        aton_pp_prac: models.aton.nodes.pp_prac.PP_PRAC = models.aton.nodes.pp_prac.PP_PRAC(prac_id=pp_prac.id)
        practitioner.set_portico_source(aton_pp_prac)
        organization.add_practitioner(practitioner)
        for prac_net_cycle in pp_prac.networks:
            log.info(f"Practitioner network cycle - {prac_net_cycle}")
            log.info(f"Practitioner network - {prac_net_cycle.network}")
            for loc_cycle in prac_net_cycle.loc_cycles:
                log.info(f"Practitioner location cycle - {loc_cycle}")
                log.info(f"Practitioner location - {loc_cycle.location}")