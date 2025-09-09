from sqlalchemy import select, Sequence
from sqlalchemy.orm import joinedload, Session

from models.portico import PPProvTinLoc, PPProvLocAttrib, PPProvLocAttribValues
from models.portico.pp_prov import PPProv
from models.portico.pp_addr import PPAddr
from models.portico.pp_prov_addr import PPProvAddr
from models.portico.pp_addr_phones import PPAddrPhones
from models.portico.pp_prov_attrib_values import PPProvAttribValues
from models.portico.pp_prov_tin import PPProvTIN
from models.portico.pp_net import PPNet

from models.portico.pp_prov_attrib import PPProvAttrib
from models.portico.pp_prov_loc import PPProvLoc
import logging

from models.portico.pp_prov_net_cycle import PPProvNetCycle
from models.portico.pp_prov_net_loc_cycle import PPProvNetLocCycle

log = logging.getLogger(__name__)


def read_provider(session:Session) -> list[PPProv] | None:
    stmt = (
        select(PPProv)
        .options(
            joinedload(PPProv.addresses)
            .joinedload(PPProvAddr.address)
            .joinedload(PPAddr.phones)
            .joinedload(PPAddrPhones.phone),
            joinedload(PPProv.prov_type),
            joinedload(PPProv.tin),
            joinedload(PPProv.attributes).joinedload(PPProvAttrib.attribute_type),
            joinedload(PPProv.attributes).joinedload(PPProvAttrib.values).joinedload(PPProvAttribValues.field),
            joinedload(PPProv.prov_locs)
                .joinedload(PPProvLoc.location)
                .joinedload(PPProvTinLoc.address)
                .joinedload(PPAddr.phones)
                .joinedload(PPAddrPhones.phone),
            joinedload(PPProv.networks).joinedload(PPProvNetCycle.network),
            joinedload(PPProv.networks).joinedload(PPProvNetCycle.loc_cycles).joinedload(PPProvNetLocCycle.location),
            joinedload(PPProv.loc_attributes).joinedload(PPProvLocAttrib.location),
            joinedload(PPProv.loc_attributes).joinedload(PPProvLocAttrib.values).joinedload(PPProvLocAttribValues.field)
        )
    )
    providers: list[PPProv] = list(session.execute(stmt).unique().scalars().all())
    log.info(f"Read providers successfully:{providers}")
    return providers

