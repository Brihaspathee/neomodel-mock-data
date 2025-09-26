from neomodel import StructuredNode, StringProperty, DateProperty, RelationshipFrom

from models.aton.nodes.base_node import BaseNode


class Qualification(BaseNode):
    type = StringProperty(required=True)
    issuer = StringProperty(required=False)
    state = StringProperty(required=False)
    status = StringProperty(required=False)
    value = StringProperty(required=False)
    start_date = DateProperty(required=False)
    end_date = DateProperty(required=False)
    secondary_label: str = ""

    organization = RelationshipFrom("models.aton.nodes.organization.Organization", "HAS_QUALIFICATION")
    location = RelationshipFrom("models.aton.nodes.location.Location", "HAS_QUALIFICATION")

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
        self._add_secondary_label()
        return node
