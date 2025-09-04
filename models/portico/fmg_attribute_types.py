from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.portico.base import Base


class FmgAttributeType(Base):
    """
    Represents the type of an attribute in a specific domain.

    Defines the structure and relationships for an attribute type in the
    system. This class includes metadata and descriptive fields, and models
    the relationship to provider attributes, serving as a central entity
    for managing attribute metadata.

    :ivar id: The unique identifier for the attribute type.
    :type id: int
    :ivar metatype: The category or classification of the attribute type.
    :type metatype: str
    :ivar description: A brief description of the attribute type.
    :type description: str
    :ivar provider_attributes: The related provider attributes associated
        with this attribute type.
    :type provider_attributes: list
    """
    __tablename__ = "fmg_attribute_types"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    metatype = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # provider_attributes = relationship("PPProvAttrib", back_populates="attribute_type")

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging purposes.

        The method returns a formatted string that includes details about the object's
        `id`, `metatype`, and `description` attributes. This representation is particularly
        useful for debugging by offering a human-readable way to inspect an instance's state.

        :return: A string representation of the object including its `id`, `metatype`,
            and `description`.
        :rtype: str
        """
        return f"<FmgAttributeType(id={self.id}, metatype={self.metatype}, description={self.description})>"
