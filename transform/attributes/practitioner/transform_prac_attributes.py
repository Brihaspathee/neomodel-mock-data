from models.aton.nodes.practitioner import Practitioner
from models.portico import PPPrac

import logging

log = logging.getLogger(__name__)


def transform_prac_attributes(pp_prac:PPPrac, practitioner:Practitioner):
    pass

def transform_prac_node(attribute_id: int, source_prac: Practitioner, destination_prac: Practitioner):
    log.info(f"Transforming attribute {attribute_id}")
    if attribute_id == 103877:
        destination_prac.altFirstName = source_prac.altFirstName
        destination_prac.middle_name = source_prac.middle_name
        destination_prac.altLastName = source_prac.altLastName
    elif attribute_id == 100039:
        if source_prac.race:
            if destination_prac.race is None:
                destination_prac.race = []
            destination_prac.race.append(source_prac.race)
        if source_prac.ethnicity:
            if destination_prac.ethnicity is None:
                destination_prac.ethnicity = []
            destination_prac.ethnicity.append(source_prac.ethnicity)
