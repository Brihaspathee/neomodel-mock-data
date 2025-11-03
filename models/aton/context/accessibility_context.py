import weakref

from models.aton.nodes.validation import Validation


class AccessibilityContext:

    def __init__(self):
        self._validation: Validation | None = None

    def set_validation(self, validation: Validation):
        self._validation = validation

    def get_validation(self) -> Validation:
        return self._validation
