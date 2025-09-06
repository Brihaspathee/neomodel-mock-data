from models.aton.nodes.location import Location
from models.aton.nodes.validation import Validation
from repository.validation_repo import find_location_by_key, create_validation
import logging

log = logging.getLogger(__name__)


def get_or_create_location(location:Location):
    validation: Validation = location.get_pending_validation()
    log.info(f"Location {location.name} needs validation, validation key is: {validation.validation_key}")
    if not validation:
        raise Exception("Location needs validation")
    location_in_db, val = find_location_by_key(validation.validation_key)
    if location_in_db:
        return location_in_db
    else:
        saved_loc = location.save()
        saved_val = create_validation(validation)
        log.info(f"connecting location {saved_loc} to validation {saved_val}")
        saved_val.location.connect(saved_loc)
        log.info(f"connected location {saved_loc} to validation {saved_val}")
        return saved_loc