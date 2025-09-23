import logging

import models
from models.aton.nodes.address import Address
from models.aton.nodes.contact import Contact
from models.aton.nodes.hours_of_operation import HoursOfOperation
from models.aton.nodes.location import Location
from models.aton.nodes.telecom import Telecom
from models.aton.nodes.validation import Validation
from utils.address_util import portico_address_to_aton, get_state
from utils.location_util import get_hash_key_for_prov_tin_loc
from models.aton.nodes.organization import Organization
from models.aton.nodes.role_instance import RoleInstance
from models.aton.nodes.role_location import RoleLocation
from models.portico import PPProv, PPProvLoc, PPProvTinLoc, PPProvLocOfHours
from transform.transform_provider_net_cycle import transform_provider_net_cycle
from transform.transform_attribute import get_prov_loc_attributes
from utils.office_hours import format_office_hours

log = logging.getLogger(__name__)

def transform_provider_location(provider: PPProv, organization:Organization):
    """
    Transforms provider location based on the given provider and organization.
    This function processes the provider's locations and networks, updates the
    corresponding role instance, and adds it to the organization.

    :param provider: The provider containing location and network information
    :param organization: The organization to which the transformed role instance
        will be added
    :return: None
    """
    if provider.prov_locs or provider.networks:
        # ------------------------------------------------------------------------------
        # When there are any locations or networks directly associated with the provider,
        # then a RoleInstance node should be created with the role type "HAS_ROLE"
        # ------------------------------------------------------------------------------
        log.debug("Transforming Portico Provider Location")
        role_instance: RoleInstance = RoleInstance()
        role_instance.set_role_type("has_role")
        if provider.prov_locs:
            # ------------------------------------------------------------------------------
            # Process the provider locations
            # ------------------------------------------------------------------------------
            _process_prov_locs(provider, role_instance)
        if provider.networks:
            # ------------------------------------------------------------------------------
            # Process the provider networks
            # ------------------------------------------------------------------------------
            log.debug("Transforming Portico Provider Network")
            transform_provider_net_cycle(provider.networks, role_instance)
        # ------------------------------------------------------------------------------
        # Add the role instance to the organization
        # ------------------------------------------------------------------------------
        organization.add_role_instance(role_instance)

def _process_prov_locs(pp_prov:PPProv, role_instance: RoleInstance):
    """
    Processes a list of provider locations and associates them with a role instance.

    This function iterates through the provided list of provider locations, creating
    an instance of `RoleLocation` for each, and sets the location details using a
    hash key generated from the provider's location details. The resulting
    `RoleLocation` objects are associated with the provided role instance. Logging is
    performed to provide insights into key operation points such as the processed
    addresses and generated hash codes.

    :param prov_locs:
        A list of `PPProvLoc` objects representing the provider locations to process.
    :param role_instance:
        An instance of `RoleInstance` where the processed role locations should
        be associated.
    :return:
        This function does not return a value.
    """
    for prov_loc in pp_prov.prov_locs:
        # ------------------------------------------------------------------------------
        # Create a new RoleLocation instance for each provider location
        # Set the location details using a hash key generated from the provider's location details'
        # Add the role location to the role instance
        # ------------------------------------------------------------------------------
        role_location: RoleLocation = RoleLocation()
        if prov_loc.PRIMARY == "Y":
            role_location.set_is_primary(True)
        prov_tin_loc: PPProvTinLoc = prov_loc.location
        log.debug(f"Location Address:{prov_tin_loc.address}")
        hash_code = get_hash_key_for_prov_tin_loc(prov_tin_loc=prov_tin_loc)
        log.debug(f"Hash Code:{hash_code}")
        location = set_location(hash_code, prov_tin_loc)
        role_location.set_location(location)
        contact: Contact = get_location_phone(prov_tin_loc)
        get_prov_loc_attributes(pp_prov, prov_tin_loc, role_location)
        role_location.add_contact(contact)
        get_prov_loc_office_hours(pp_prov, prov_tin_loc, role_location)
        role_instance.add_pending_rl(role_location)
        log_role_location_contacts(role_location=role_location)


def set_location(hash_code, prov_tin_loc) -> Location:
    """
    Sets the location details for a given hash code and provider location information
    and initializes a Location object with the specified attributes.

    :param hash_code: A unique string identifier used for address validation.
        This is used as the validation key while setting the pending validation
        for the created `Location` object.
    :type hash_code: str
    :param prov_tin_loc: A provider location object containing the details
        of the location such as name, address, city, state, ZIP code, county,
        FIPS code, latitude, and longitude.
    :type prov_tin_loc: ProviderLocation
    :return: A `Location` object populated with the details from the given
        `prov_tin_loc` and validated using the `hash_code`.
    :rtype: Location
    """
    location: Location = Location()
    log.debug(f"Location name:{prov_tin_loc.name}")
    portico_location: models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC = models.aton.nodes.pp_prov_tin_loc.PP_PROV_TIN_LOC(loc_id=str(prov_tin_loc.id))
    location.set_portico_source(portico_location)
    location.name = prov_tin_loc.name
    location.street_address = prov_tin_loc.address.addr1
    location.secondary_address = prov_tin_loc.address.addr2
    location.city = prov_tin_loc.address.city.ds
    if prov_tin_loc.address.county_fips:
        location.state = get_state(prov_tin_loc.address.county_fips)
    else:
        location.state = "COUNTY NOT AVAILABLE"
    location.zip_code = prov_tin_loc.address.zip
    location.county = prov_tin_loc.address.county.ds
    location.county_fips = prov_tin_loc.address.county_fips
    location.latitude = prov_tin_loc.address.latitude
    location.longitude = prov_tin_loc.address.longitude
    # ------------------------------------------------------------------------------
    # Set pending validation for the location
    # ------------------------------------------------------------------------------
    validation: Validation = Validation(type="address", source="smartystreets", validation_key=hash_code)
    location.set_pending_validation(validation)
    return location


def get_location_phone(pp_prov_tin_loc:PPProvTinLoc) -> Contact:
    contact: Contact = Contact()
    contact.use = "Directory"
    if pp_prov_tin_loc.address:
        loc_address = pp_prov_tin_loc.address
        if loc_address.phones:
            telecom: Telecom = Telecom()
            for addr_phone in loc_address.phones:
                log.debug(f"Location phone is {addr_phone}")
                log.debug(f"Location phone is {addr_phone.phone}")
                if addr_phone.phone.type == "PHONE":
                    telecom.phone = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "FAX":
                    telecom.fax = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "TTY":
                    telecom.tty = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
                elif addr_phone.phone.type == "AFH":
                    telecom.afterHoursNumber = addr_phone.phone.areacode + addr_phone.phone.exchange + addr_phone.phone.num
            contact.set_pending_telecom(telecom)
    return contact

def get_prov_loc_office_hours(provider:PPProv, pp_prov_tin_loc:PPProvTinLoc, role_location:RoleLocation):
    # converted_office_hours = format_office_hours(prov_loc_office_hours=provider.loc_ofhours)
    # log.error(f"Converted office hours - {converted_office_hours}")
    prov_loc_office_hours: list[PPProvLocOfHours] = []
    for prov_loc_ofhours in provider.loc_ofhours:
        location: PPProvTinLoc = prov_loc_ofhours.location
        if location.id == pp_prov_tin_loc.id:
            prov_loc_office_hours.append(prov_loc_ofhours)
    converted_office_hours = format_office_hours(prov_loc_office_hours=prov_loc_office_hours)
    log.debug(f"Converted office hours - {converted_office_hours}")
    if not converted_office_hours:
        return
    is_office_hours_set = False
    if role_location.get_pending_contacts():
        for contact in role_location.get_pending_contacts():
            if contact.use == "Directory":
                hours_of_operation: HoursOfOperation = HoursOfOperation(hours=converted_office_hours)
                contact.set_pending_hours_of_operation(hours_of_operation)
                is_office_hours_set = True
                break
    if not is_office_hours_set:
        contact: Contact = Contact()
        contact.use = "Directory"
        hours_of_operation: HoursOfOperation = HoursOfOperation(hours=converted_office_hours)
        contact.set_pending_hours_of_operation(hours_of_operation)
        role_location.add_contact(contact)

def log_role_location_contacts(role_location: RoleLocation):
    if role_location.get_pending_contacts():
        for contact in role_location.get_pending_contacts():
            log.info(f"Contact: {contact}")
            log.info(f"Contact Use: {contact.use}")
            log.info(f"Contact Hours of operation: {contact.get_pending_hours_of_operation()}")





