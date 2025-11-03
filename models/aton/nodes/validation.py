from datetime import date

from neomodel import StructuredNode, StringProperty, RelationshipTo, DateProperty

from models.aton.nodes.base_node import BaseNode
from models.aton.nodes.node_utils import convert_dates_to_native


class Validation(BaseNode):

    type: str = StringProperty(required=True)
    source: str = StringProperty(required=True)
    validation_key: str = StringProperty(required=False)
    validation_date = DateProperty(required=False, default=lambda: date.today())

    location = RelationshipTo("models.aton.nodes.location.Location", "VALIDATED")
    accessibility = RelationshipTo("models.aton.nodes.accessibility.Accessibility", "VALIDATED")

    def save(self, *args, **kwargs):
        node = super().save(*args, **kwargs)
        convert_dates_to_native(node)
        return node