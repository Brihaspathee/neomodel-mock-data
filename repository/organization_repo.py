from models.aton.nodes.identifier import LegacySystemID
from models.aton.nodes.pp_prov import PP_PROV


def get_organization_by_prov_id(prov_id:str):
    pp_prov = LegacySystemID.nodes.get_or_none(value=prov_id,
                                               system="PORTICO",
                                               systemIdType="PROV ID")
    if not pp_prov:
        return None
    return pp_prov.aton_org.single()