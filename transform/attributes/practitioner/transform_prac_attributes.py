from models.aton.nodes.practitioner import Practitioner
from models.portico import PPPrac


def transform_prac_attributes(pp_prac:PPPrac, practitioner:Practitioner):
    pass

def transform_prac_node(attribute_id: int, source_prac: Practitioner, destination_prac: Practitioner):
    if attribute_id == 103877:
        destination_prac.altFirstName = source_prac.altFirstName
        destination_prac.middle_name = source_prac.middle_name
        destination_prac.altLastName = source_prac.altLastName
    elif attribute_id == 100039:
        destination_prac.race.__add__(source_prac.race)
        destination_prac.ethnicity.__add__(source_prac.ethnicity)