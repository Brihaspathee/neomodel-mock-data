from datetime import date

from config.privilege_settings import PRIVILEGE_TYPE_MAPPING
from config.map_reader.cred_type_geo_map import CRED_TYPE_GEO_MAPPING
from models.aton.context.practitioner_context import PractitionerContext, HospitalPrivilege
from models.aton.context.role_instance_context import RoleInstanceContext
from models.aton.nodes.credentialing import Credentialing
from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.organization import Organization
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.role_instance import RoleInstance
from models.portico import PPProv, PPPrac, PPPracLoc, PPPracCredCycle
import logging

from transform.attributes.transform_attribute import transform_attributes
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
        practitioner.context = PractitionerContext(practitioner)
        for hosp_priv in pp_prac.hosp_privileges:
            log.debug(f"Practitioner Hospital Privileges: {hosp_priv}")
            if hosp_priv.priv_exp_date is None or hosp_priv.priv_exp_date > date.today():
                if hosp_priv.privilege is not None and get_hosp_priv_type(hosp_priv.privilege) is not None:
                    hosp_priv_obj: HospitalPrivilege = HospitalPrivilege(privilegeType=get_hosp_priv_type(hosp_priv.privilege),
                                                                         prov_id=str(hosp_priv.prov_id))
                    practitioner.context.add_privilege(hosp_priv_obj)
        for cred_cycle in pp_prac.cred_cycles:
            credentialing: Credentialing = get_prac_cred(cred_cycle)
            if credentialing is not None:
                practitioner.context.add_credential(credentialing)
        role_instance: RoleInstance = RoleInstance()
        role_instance.context = RoleInstanceContext(role_instance)
        practitioner.context.set_role_instance(role_instance)
        aton_pp_prac: LegacySystemIdentifier = LegacySystemIdentifier(value=pp_prac.id,
                                                                      system="PORTICO",
                                                                      systemIdType="PRAC ID")
        practitioner.context.set_portico_source(aton_pp_prac)
        transform_attributes("PRACTITIONER", pp_prac, practitioner)
        organization.context.add_practitioner(practitioner)
        transform_practitioner_location(pp_prac, role_instance, pp_prov.id)


def get_distinct_pracs(pp_prac_locs:list[PPPracLoc]) -> list[PPPrac]:
    pracs: list[PPPrac] = []
    for pp_prac_loc in pp_prac_locs:
        pp_prac: PPPrac = pp_prac_loc.practitioner
        if pp_prac not in pracs:
            pracs.append(pp_prac)
    return pracs

def get_hosp_priv_type(portico_type:str) -> str | None:
    try:
        return PRIVILEGE_TYPE_MAPPING[portico_type]
    except KeyError:
        return None

def get_prac_cred(pp_prac_cred_cycle: PPPracCredCycle) -> Credentialing | None:
    log.info(f"Practitioner credential cycle - {pp_prac_cred_cycle}")
    cred_type: str = pp_prac_cred_cycle.cred_type
    try:
        cred_type_geo: dict[str, str] = CRED_TYPE_GEO_MAPPING[cred_type]
        cred_type_ds: str = cred_type_geo.get("description")
        if cred_type_ds is not None:
            prac_cred_type: str = get_cred_type(cred_type_ds)
            geo_desc = cred_type_geo.get("geography_description")
            geo_fips = cred_type_geo.get("FIPS")
            is_cred_delegated = False
            cred_organization: str | None = None
            cred_delegated = pp_prac_cred_cycle.is_delegated_cred
            if cred_delegated == 'Y':
                is_cred_delegated = True
                cred_organization = pp_prac_cred_cycle.affiliated_agency
            credentialing: Credentialing = Credentialing(cred_type=prac_cred_type,
                                                         geography_description=geo_desc,
                                                         fips=geo_fips,
                                                         cred_delegated=is_cred_delegated,
                                                         cred_organization=cred_organization)
            return credentialing
        else:
            return None
    except KeyError:
        log.info(f"No geo mapping found for credential type {cred_type}")
        return None

def get_cred_type(value:str) -> str | None:
    if value is None:
        return None
    if "Recredentialing" in value:
        return "RECREDENTIALING"
    elif "Provisional" in value:
        return "PROVISIONAL"
    else:
        return "INITIAL"