from models.aton.nodes.identifier import LegacySystemIdentifier


def get_practitioner_by_prac_id(prac_id:str):
    pp_prac = LegacySystemIdentifier.nodes.get_or_none(value=prac_id, system="PORTICO", systemIdType="PRAC ID")
    if not pp_prac:
        return None
    return pp_prac.practitioner.single()