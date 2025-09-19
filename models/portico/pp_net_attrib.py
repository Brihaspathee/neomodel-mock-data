from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base
from typing import List, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from models.portico.pp_net_attrib_values import PPNetAttribValues, PPNetAttribValueDict


class PPNetAttribDict(TypedDict, total=False):
    id: str
    attribute_id: str | None
    attribute_type: str | None
    values: list["PPNetAttribValueDict"]

class PPNetAttrib(Base):

    __tablename__ = "pp_net_attrib"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    net_id = Column(Integer, ForeignKey("portown.pp_net.id"))
    attribute_id = Column(Integer, ForeignKey("portown.fmg_attrib_types.id"))

    net = relationship("PPNet", back_populates="attributes")
    values: Mapped[List["PPNetAttribValues"]] = relationship("PPNetAttribValues")
    attribute_type = relationship("FmgAttributeType")

    def to_dict(self) -> PPNetAttribDict:
        return {
            "id": str(self.id),
            "attribute_id": str(self.attribute_type.id),
            "attribute_type": self.attribute_type.metatype if self.attribute_type else None,
            "values": [v.to_dict() for v in self.values],
        }

    def __repr__(self):
        return f"<PPNetAttrib(id={self.id}, net_id={self.net_id}, attribute_id={self.attribute_id})>"