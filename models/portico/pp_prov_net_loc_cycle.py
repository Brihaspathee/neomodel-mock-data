from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPProvNetLocCycle(Base):

    __tablename__ = "pp_prov_net_loc_cycle"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prov_net_cycle_id = Column(Integer, ForeignKey("portown.pp_prov_net_cycle.id"))
    loc_id = Column(Integer, ForeignKey("portown.pp_prov_tin_loc.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    prov_net_cycle = relationship("PPProvNetCycle", back_populates="loc_cycles")
    location = relationship("PPProvTinLoc")

    def __repr__(self):
        return (f"<PPProvNetLocCycle(id={self.id}, "
                f"prov_net_cycle_id={self.prov_net_cycle_id}, "
                f"loc_id={self.loc_id}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date})>")