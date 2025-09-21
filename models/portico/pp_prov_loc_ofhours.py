from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from models.portico.base import Base

if TYPE_CHECKING:
    from models.portico.pp_prov import PPProv
    from models.portico.pp_prov_tin_loc import PPProvTinLoc


class PPProvLocOfHours(Base):

    __tablename__ = "pp_prov_loc_ofhours"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"))
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"))
    event = Column(String, nullable=False)
    dayofweek = Column(String, nullable=False)
    time = Column(String, nullable=False)

    # Relationships
    provider: Mapped["PPProv"] = relationship("PPProv", back_populates="loc_ofhours")
    location: Mapped["PPProvTinLoc"] = relationship("PPProvTinLoc")  # one-way


    def __repr__(self):
        return (f"<PPProvLocOfHours(id={self.id}, "
                f"prov_id={self.prov_id}, "
                f"loc_id={self.loc_id}, "
                f"event={self.event}, "
                f"dayofweek={self.dayofweek}, "
                f"time={self.time})>")