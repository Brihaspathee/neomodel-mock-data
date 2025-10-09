import importlib
from typing import Any

from neomodel import StructuredNode

from config.attribute_settings import ATTRIBUTES_CONFIG, SPECIAL_ATTRIBUTES
from config.attributes_mapping import AttributeMapping
from models.aton.nodes.identifier import NPI, Identifier, PPGID
from models.aton.nodes.location import Location
from models.aton.nodes.network import Network
from models.aton.nodes.organization import Organization
from models.aton.nodes.organization_context import OrganizationContext
from models.aton.nodes.practitioner import Practitioner
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.aton.nodes.role_specialty import RoleSpecialty
from models.portico import PPProv, PPProvTinLoc, PPNet, PPPrac, PPProvAttrib
from transform.attributes.provider.transform_prov_attribute import  get_provider_attributes as _get_prov_attributes
from transform.attributes.practitioner.transform_prac_attributes import get_prac_attributes as _get_prac_attributes
from transform.attributes.network.transform_network_attribute import get_net_attributes as _get_net_attributes
from transform.attributes.provider.location.transform_prov_loc_attribute import get_prov_loc_attributes as _get_prov_loc_attributes
from transform.attributes.practitioner.location.transform_prac_loc_attributes import get_prac_loc_attributes as _get_prac_loc_attributes
import portico_reads.service.fmg_codes.load_fmg_codes as fmg_loader
import logging

from models.portico.pp_net import PPNetDict

log = logging.getLogger(__name__)

def transform_attributes(attr_type: str, *args):
    if attr_type == "NETWORK":
        _get_net_attributes(*args)
    elif attr_type == "PROVIDER":
        _get_prov_attributes(*args)
    elif attr_type == "PROV_LOC":
        _get_prov_loc_attributes(*args)
    elif attr_type == "PRACTITIONER":
        _get_prac_attributes(*args)
    elif attr_type == "PRAC_LOC":
        _get_prac_loc_attributes(*args)