from neomodel import db

from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.location import Location
from models.aton.nodes.qualification import Qualification
from models.aton.nodes.validation import Validation
from repository.validation_repo import find_location_by_key, create_validation
import logging

log = logging.getLogger(__name__)


def get_or_create_location(location:Location):
    validation: Validation = location.get_pending_validation()
    log.debug(f"Location {location.name} needs validation, validation key is: {validation.validation_key}")
    if not validation:
        raise Exception("Location needs validation")
    location_in_db, val = find_location_by_key(validation.validation_key)
    if location_in_db:
        check_for_qualification_updates(location_in_db, location)
        return location_in_db
    else:
        # saved_loc = location.save()
        location.save()
        saved_val = create_validation(validation)
        create_qualifications(location)
        prov_tin_loc: LegacySystemID = location.get_portico_source().save()
        prov_tin_loc.location.connect(location)
        log.debug(f"connecting location {location} to validation {saved_val}")
        saved_val.location.connect(location)
        log.debug(f"connected location {location} to validation {saved_val}")
        return location

def check_for_qualification_updates(existing_location:Location, updated_location:Location):
    new_quals = updated_location.get_pending_qualifications()
    new_quals.sort(key=lambda x: x.type)
    query = """
            MATCH (loc:Location)-[:HAS_QUALIFICATION]->(q)
            WHERE elementId(loc) = $loc_id
            RETURN q
        """
    results, _ = db.cypher_query(query, {"loc_id": existing_location.element_id})
    # Convert raw nodes to Neomodel objects
    existing_loc_quals = [Qualification.inflate(row[0]) for row in results]
    existing_loc_quals.sort(key=lambda q: q.type)
    log.debug(f"Existing quals: {existing_loc_quals}")
    log.debug(f"New quals: {new_quals}")
    for new_qual in new_quals:
        is_qual_updated(new_qual, existing_loc_quals, existing_location)

def is_qual_updated(new_qual: Qualification,
                    existing_quals: list[Qualification],
                    loc:Location) -> None:
    is_existing_qual = False
    same_type_existing_quals = []
    for existing_qual in existing_quals:
        if new_qual.type == existing_qual.type:
            is_existing_qual = True
            # Compare the value, issuer and start date to see if a new one of the same type needs to be created
            if (new_qual.value != existing_qual.value or
                    new_qual.issuer != existing_qual.issuer or
                    new_qual.start_date != existing_qual.start_date):
                new_qual.save()
                loc.qualifications.connect(new_qual)
                return None
            # if they are all the same, add the qualification to the list of existing quals
            # if the end date or the status of the qualification has changed.
            elif (new_qual.end_date != existing_qual.end_date or
                  new_qual.status != existing_qual.status):
                same_type_existing_quals.append(existing_qual)
    # If the qualification is an existing qualification, then if something was changed,
    # it was immediately saves and returned. If only the end date was changed, then
    # it is added to the list of existing quals to compare with the end date. If
    # nothing has changed, then no update is needed for the qualification.
    if not is_existing_qual:
        # If it is not an existing qualification, then create a new one.
        new_qual.save()
        loc.qualifications.connect(new_qual)
    elif len(same_type_existing_quals) > 0:
        # if it is an existing qualification, then compare the end date with the existing ones of the same type.
        # retrieve the latest qualification of the same type and update its end date.
        latest_qual = max(same_type_existing_quals, key=lambda o: o.end_date)
        latest_qual.end_date = new_qual.end_date
        latest_qual.status = new_qual.status
        latest_qual.save()
    return None

def create_qualifications(loc: Location):
    log.debug(
        f"Writing qualifications to Aton for location {loc.name}"
        f"Qualifications are: {loc.get_pending_qualifications()}"
    )
    rel = getattr(loc, "qualifications")
    for qual_node in loc.get_pending_qualifications():
        if not hasattr(qual_node, "element_id") or qual_node.element_id is None:
            qual_node.save()
            log.debug(f"Qualification saved to Aton its element id is: {qual_node.element_id}")
            rel.connect(qual_node)
