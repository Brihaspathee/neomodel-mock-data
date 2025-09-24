from models.aton.nodes.pp_prac import PP_PRAC


def get_practitioner_by_prac_id(prac_id:str):
    pp_prac = PP_PRAC.nodes.get_or_none(prac_id=prac_id)
    if not pp_prac:
        return None
    return pp_prac.aton_prac.single()