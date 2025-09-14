from models.aton.nodes.pp_prov import PPProv


def get_organization_by_prov_id(prov_id:str):
    pp_prov = PPProv.nodes.get_or_none(prov_id=prov_id)
    if not pp_prov:
        return None
    return pp_prov.aton_org.single()