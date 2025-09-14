from neomodel import StructuredNode, StringProperty, RelationshipTo


class PPProv(StructuredNode):
    __label__ = "PP_Prov"
    prov_id = StringProperty(required=True)

    aton_org = RelationshipTo("models.aton.nodes.organization.Organization", "SOURCES")