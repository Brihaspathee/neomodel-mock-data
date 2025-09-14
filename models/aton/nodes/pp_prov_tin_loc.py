from neomodel import StringProperty, RelationshipTo, StructuredNode

class PPProvTINLoc(StructuredNode):
    __label__ = "PP_Prov_TIN_Loc"
    loc_id = StringProperty(required=True)

    aton_location = RelationshipTo("models.aton.nodes.location.Location", "SOURCES")