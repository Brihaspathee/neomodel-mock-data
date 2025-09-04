from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base

# if TYPE_CHECKING:
#     from models.portico import PPNet


class PPProvNetCycle(Base):

    __tablename__ = "pp_prov_net_cycle"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"))
    net_id = Column(Integer, ForeignKey("portown.pp_net.id"))
    status = Column(String, nullable=False)

    provider = relationship("PPProv", back_populates="networks")
    network = relationship("PPNet")
    loc_cycles = relationship("PPProvNetLocCycle", back_populates="prov_net_cycle")