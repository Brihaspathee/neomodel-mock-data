from transform.attributes.provider.transform_prov_attribute import  get_provider_attributes as _get_prov_attributes
from transform.attributes.practitioner.transform_prac_attributes import get_prac_attributes as _get_prac_attributes
from transform.attributes.network.transform_network_attribute import get_net_attributes as _get_net_attributes
from transform.attributes.provider.location.transform_prov_loc_attribute import get_prov_loc_attributes as _get_prov_loc_attributes
from transform.attributes.practitioner.location.transform_prac_loc_attributes import get_prac_loc_attributes as _get_prac_loc_attributes
import logging

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