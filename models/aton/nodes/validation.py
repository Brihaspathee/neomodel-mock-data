from neomodel import StructuredNode, StringProperty, RelationshipTo


class Validation(StructuredNode):

    type: str = StringProperty(required=True)
    source: str = StringProperty(required=True)
    validation_key: str = StringProperty(required=True)

    location = RelationshipTo("models.aton.nodes.location.Location", "VALIDATED")