from datetime import date

from neomodel import StructuredNode, StringProperty, DateProperty, RelationshipFrom, db, ArrayProperty

from models.aton.nodes.base_node import BaseNode
import logging

from models.aton.nodes.node_utils import convert_dates_to_native

log = logging.getLogger(__name__)

class Qualification(BaseNode):
    type = StringProperty(required=True)
    issuer = StringProperty(required=False)
    state = StringProperty(required=False)
    status = StringProperty(required=False)
    value = StringProperty(required=False)
    start_date = DateProperty(required=False, db_property="startDate")
    end_date = DateProperty(required=False, db_property="endDate")
    level = ArrayProperty(required=False, db_property="level")
    secondary_label: str = ""

    organization = RelationshipFrom("models.aton.nodes.organization.Organization", "HAS_QUALIFICATION")
    location = RelationshipFrom("models.aton.nodes.location.Location", "HAS_QUALIFICATION")

    practitioner = RelationshipFrom("models.aton.nodes.practitioner.Practitioner", "HAS_QUALIFICATION")

    def _add_secondary_label(self):
        if self.secondary_label:
            query = f"""
                MATCH (n)
                WHERE elementId(n) = $element_id
                SET n:`{self.secondary_label}`
                """
            self.cypher(query, {"element_id": self.element_id})

    def save(self, *args, **kwargs):
        node = super().save(*args, **kwargs)
        log.debug(f"Node saved: {node}")
        self._add_secondary_label()
        convert_dates_to_native(node)
        return node
