from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.portico.base import Base


class FmgAttributeField(Base):
    """
    Represents a field in FMG attribute management system in the database.

    The `FmgAttributeField` class is a mapped ORM class that represents a field
    in the FMG attribute system. This field contains information about
    attributes and metadata, including names, data types, and optional codes.
    Its purpose is to define the structure of the FMG attributes as represented
    in the database schema. Relationships with other tables are also defined
    here to model corresponding associations.

    :ivar id: The unique identifier for each FMG attribute field.
    :type id: int
    :ivar attribute_id: The ID of the associated attribute.
    :type attribute_id: int
    :ivar fmgcode: An optional FMG code associated with the attribute field.
    :type fmgcode: str or None
    :ivar field_name: The name of the field associated with the FMG attribute.
    :type field_name: str
    :ivar datatype: The data type of the field, such as string, integer, etc.
    :type datatype: str
    :ivar values: A relationship to `PPProvAttribValues` that represents the
        associated attribute values.
    :type values: sqlalchemy.orm.relationship
    """
    __tablename__ = "fmg_attrib_fields"
    __table_args__ = {"schema": "portown"}


    id = Column(Integer, primary_key=True)
    attribute_id = Column(Integer, nullable=False)
    fmgcode = Column(String, nullable=True)
    fieldname = Column(String, nullable=False)
    datatype = Column(String, nullable=False)

    # values = relationship("PPProvAttribValues", back_populates="field")

    def __repr__(self):
        """
        Represents the string representation of the FmgAttributeField instance.

        The `__repr__` method provides a developer-friendly string representation
        of an instance, typically used for debugging purposes. This includes key
        attributes of the FmgAttributeField such as `id`, `attribute_id`, `fmgcode`,
        `field_name`, and `datatype`.

        :return: A string representation of the FmgAttributeField instance,
            formatted with its key attributes.
        :rtype: str
        """
        return f"<FmgAttributeField(id={self.id}, attribute_id={self.attribute_id}, fmgcode={self.fmgcode}, field_name={self.fieldname}, datatype={self.datatype})>"