from neomodel import StringProperty, StructuredRel


class HasPrivilege(StructuredRel):
    privilege_type = StringProperty(required=True, db_property="privilegeType")