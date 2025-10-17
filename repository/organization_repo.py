from models.aton.nodes.identifier import LegacySystemIdentifier
from models.aton.nodes.organization import Organization


def get_organization_by_prov_id(prov_id:str) -> Organization | None:
    pp_prov = LegacySystemIdentifier.nodes.get_or_none(value=prov_id,
                                                       system="PORTICO",
                                                       systemIdType="PROV ID")
    if not pp_prov:
        return None
    return pp_prov.organization.single()