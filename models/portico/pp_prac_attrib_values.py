from sqlalchemy import Column, Integer, ForeignKey, String, Date, Numeric
from sqlalchemy.orm import Mapped, relationship

from models.portico import Base


class PPPracAttribValues(Base):
    __tablename__ = "pp_prac_attrib_values"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_attribute_id = Column(Integer, ForeignKey("portown.pp_prac_attrib.id"))
    field_id = Column(Integer, ForeignKey("portown.fmg_attrib_fields.id"))
    value = Column(String, nullable=True)
    value_date = Column(Date, nullable=True)
    value_number = Column(Numeric, nullable=True)

    field: Mapped["FmgAttributeField"] = relationship("FmgAttributeField")

    def __repr__(self):
        return (f"<PPPracAttribValues(id={self.id}, "
                f"prac_attribute_id={self.prac_attribute_id}, "
                f"field_id={self.field_id}"
                f"value={self.value}, "
                f"value_date={self.value_date}, "
                f"value_number={self.value_number})>")