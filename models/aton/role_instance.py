from neomodel import RelationshipFrom, RelationshipTo, StructuredNode


class RoleInstance(StructuredNode):

    _role_type: str = None
    organization = RelationshipFrom("models.aton.organization.Organization", "HAS_ROLE")
    contracted_organization = RelationshipTo("models.aton.organization.Organization", "CONTRACTED_BY")

    def set_role_type(self, role_type: str):
        self._role_type = role_type

    def get_role_type(self):
        return self._role_type

    def __str__(self):
        return f"Role Instance Type: {self._role_type}"