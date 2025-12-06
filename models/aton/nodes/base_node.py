import secrets
import string

from neomodel import StructuredNode, BooleanProperty, StringProperty

import logging

from utils.common_utils import generate_unique_code

log = logging.getLogger(__name__)


class BaseNode(StructuredNode):
    """
    Represents the base class for nodes in the structured data model.

    This class serves as an abstract node that can be extended by other node
    classes. It provides a shared functionality for handling mock data scenarios
    during the save operation. Specifically, it checks if mock data context is
    enabled and sets the `isMockData` attribute accordingly before saving the
    node. Instances of this class cannot be created directly due to its abstract
    nature.

    :ivar isMockData: Indicates if the current data is mock data. The value is
        set to `True` if the mock data context is enabled during the save
        operation. Defaults to `False`.
    :type isMockData: bool
    """
    __abstract_node__ = True

    isMockData = BooleanProperty(required=False)
    code = StringProperty(required=False)

    def save(self, *args, **kwargs):
        """
        Saves the current instance, handling any specific behavior depending on the context.
        This method overrides the base save method to enable mock data handling when
        certain conditions are met.

        :param args: Positional arguments to pass to the base save method
        :param kwargs: Keyword arguments to pass to the base save method
        :return: The result of calling the base save method
        """
        from .mock_context import is_mock_enabled, get_create_entity_code
        if is_mock_enabled():
            self.isMockData = True
        node_label = self.__label__
        log.debug(f"Saving {node_label} node")
        if get_create_entity_code() and (node_label == "Practitioner" or
                                       node_label == "Organization" or
                                       node_label == "Location"):
            self.code = generate_unique_code(15)
        return super().save(*args, **kwargs)

