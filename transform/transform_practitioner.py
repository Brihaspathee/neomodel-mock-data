import models
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance
from models.portico import PPProv, PPPrac, PPPracLoc
import logging

from transform.transform_practitioner_location import transform_practitioner_location

log = logging.getLogger(__name__)

def transform_practitioner(pp_prov:PPProv, organization: Organization):
    pp_pracs: list[PPPrac] = get_distinct_pracs(pp_prov.prac_locs)
    for pp_prac in pp_pracs:
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
        transform_practitioner_location(pp_prac, role_instance, pp_prov.id)


def get_distinct_pracs(pp_prac_locs:list[PPPracLoc]) -> list[PPPrac]:
    pracs: list[PPPrac] = []
    for pp_prac_loc in pp_prac_locs:
        pp_prac: PPPrac = pp_prac_loc.practitioner
        if pp_prac not in pracs:
            pracs.append(pp_prac)
    return pracs