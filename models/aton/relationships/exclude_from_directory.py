from neomodel import StructuredRel, StringProperty


class ExcludeFromDirectory(StructuredRel):
    exclude_reason = StringProperty(required=True)