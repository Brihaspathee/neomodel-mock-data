from neomodel import StructuredNode, StringProperty, RelationshipTo


class Network(StructuredNode):
    code = StringProperty(required=True)
    name = StringProperty(required=True)

    product = RelationshipTo("models.aton.product.Product", "PART_OF")