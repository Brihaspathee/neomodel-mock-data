from neomodel import DateProperty, StringProperty, StructuredRel


class RoleLocationServes(StructuredRel):
    start_date = DateProperty(required=True)
    end_date = DateProperty(required=True)
    term_reason = StringProperty(required=False)