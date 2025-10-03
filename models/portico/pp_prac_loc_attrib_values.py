from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.portico.fmg_attribute_fields import FmgAttributeField


class PPPracLocAttribValues(Base):

    __tablename__ = "pp_prac_loc_attrib_values"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_loc_attribute_id = Column(Integer, ForeignKey("portown.pp_prac_loc_attrib.id"))
    field_id = Column(Integer, ForeignKey("portown.fmg_attrib_fields.id"))
    value = Column(String, nullable=True)
    value_date = Column(Date, nullable=True)
    value_number = Column(Numeric, nullable=True)

    # provider_attribute = relationship("PPProvAttrib", back_populates="values")
    # field = relationship("FmgAttributeField", back_populates="values")
    field: Mapped["FmgAttributeField"]= relationship("FmgAttributeField")

    def __repr__(self):

        return (f"<PPPracLocAttribValues(id={self.id}, "
                f"prac_loc_attribute_id={self.prac_loc_attribute_id}, "
                f"field_id={self.field_id}, "
                f"value={self.value}, "
                f"value_date={self.value_date}, "
                f"value_number={self.value_number})>")
