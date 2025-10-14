from neomodel import DateProperty, StringProperty, StructuredRel


class RoleLocationServes(StructuredRel):
    start_date = DateProperty(required=True, db_property="startDate")
    end_date = DateProperty(required=True, db_property="endDate")
    term_reason = StringProperty(required=False, db_property="termReason")