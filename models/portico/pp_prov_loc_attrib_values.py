from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.fmg_attribute_fields import FmgAttributeField


class PPProvLocAttribValues(Base):
    """
    Represents an ORM model for provider attribute values in the "portown" schema.

    This class maps to the table "pp_prov_attrib_values" in the database, where each
    row corresponds to a specific value associated with a provider attribute. The
    values can be of different types such as a string, date, or numeric value. It
    establishes relationships with provider attributes and attribute fields, making
    it easier to query and manage these associations in a database context.

    :ivar id: Unique identifier for the attribute value entry.
    :type id: int
    :ivar prov_attribute_id: Foreign key linking to the provider attribute table.
    :type prov_attribute_id: int
    :ivar field_id: Foreign key linking to the attribute field table.
    :type field_id: int
    :ivar value: A textual representation of the value, if applicable.
    :type value: Optional[str]
    :ivar value_date: A date-type representation of the value, if applicable.
    :type value_date: Optional[datetime.date]
    :ivar value_number: A numeric representation of the value, if applicable.
    :type value_number: Optional[decimal.Decimal]
    :ivar provider_attribute: Relationship to the PPProvAttrib table, representing
        the associated provider attribute.
    :type provider_attribute: sqlalchemy.orm.RelationshipProperty
    :ivar field: Relationship to the FmgAttributeField table, representing the
        associated attribute field.
    :type field: sqlalchemy.orm.RelationshipProperty
    """
    __tablename__ = "pp_prov_loc_attrib_values"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_loc_attribute_id = Column(Integer, ForeignKey("portown.pp_prov_loc_attrib.id"))
    field_id = Column(Integer, ForeignKey("portown.fmg_attrib_fields.id"))
    value = Column(String, nullable=True)
    value_date = Column(Date, nullable=True)
    value_number = Column(Numeric, nullable=True)

    # provider_attribute = relationship("PPProvAttrib", back_populates="values")
    # field = relationship("FmgAttributeField", back_populates="values")
    field: Mapped["FmgAttributeField"]= relationship("FmgAttributeField")

    def __repr__(self):
        """
        Generate the official string representation of the PPProvAttribValues object.

        This method is intended to provide a human-readable representation of
        the instance, showing its critical attributes for debugging and logging
        purposes.

        :return: A string representation of the PPProvAttribValues instance,
            including values of its main attributes.
        :rtype: str
        """
        return (f"<PPProvLocAttribValues(id={self.id}, "
                f"prov_loc_attribute_id={self.prov_loc_attribute_id}, "
                f"field_id={self.field_id}, "
                f"value={self.value}, "
                f"value_date={self.value_date}, "
                f"value_number={self.value_number})>")
