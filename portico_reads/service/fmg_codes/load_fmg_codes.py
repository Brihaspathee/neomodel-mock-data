from collections import defaultdict

from sqlalchemy.orm import Session

from models.portico.fmg_code import FMGCode
import logging

log = logging.getLogger(__name__)

FMG_CODES: dict[str, dict[str, str]] = {}

def load_fmg_codes(session: Session):
    global FMG_CODES
    cache = defaultdict(dict)
    log.debug("Loading FMG codes")
    for row in session.query(FMGCode).all():
        # log.debug(f"FMG Code: {row.code} - {row.ds}")
        cache[row.TYPE][row.code] = row.ds
    # log.debug(f"cache: {cache}")
    # log.debug(f"cache: {dict(cache)}")
    FMG_CODES = dict(cache)
    log.debug(f"FMG_CODES: {FMG_CODES}")