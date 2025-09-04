import logging

from models.aton.organization import Organization
from models.aton.role_instance import RoleInstance
from models.portico import PPProv

log = logging.getLogger(__name__)

def transform_provider_location(provider: PPProv, organization:Organization):
    if provider.prov_locs or provider.networks:
        log.info("Transforming Portico Provider Location")
        role_instance: RoleInstance = RoleInstance()
        role_instance.set_role_type("has_role")
        organization.add_role_instance(role_instance)