from neomodel import StructuredNode, StringProperty, RelationshipTo

from models.aton.nodes.base_node import BaseNode


class Validation(BaseNode):

    type: str = StringProperty(required=True)
    source: str = StringProperty(required=True)
    validation_key: str = StringProperty(required=True)

    location = RelationshipTo("models.aton.nodes.location.Location", "VALIDATED")