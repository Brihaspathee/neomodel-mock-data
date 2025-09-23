from models.aton.nodes.location import Location
from models.aton.nodes.validation import Validation
import logging

log = logging.getLogger(__name__)


def find_location_by_key(key: str) -> tuple[Location, Validation] | tuple[None, None]:
    try:
        validation: Validation = Validation.nodes.get(validation_key=key)
        location = validation.location.single()
        if location:
            return location, validation
        else:
            return None, None
    except Validation.DoesNotExist:
        return None, None

def create_validation(validation: Validation) -> Validation:
    log.debug(f"Creating validation for {validation}")
    val = validation.save()
    log.debug(f"Saved Validation {validation}")
    return val