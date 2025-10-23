from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracHosp(Base):
    __tablename__ = "pp_prac_hosp"
    __table_args__ = {"schema": "portown"}

    prov_id = Column(Integer, ForeignKey("portown.pp_prov.id"), primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"), primary_key=True)
    privilege = Column(String, default=False)
    priv_eff_date = Column(Date, nullable=False)
    priv_exp_date = Column(Date, nullable=False)

    provider = relationship("PPProv")
    practitioner = relationship("PPPrac", back_populates="hosp_privileges")

    def __repr__(self):
        return (
            f"<PPPracHosp(prov_id={self.prov_id}, prac_id={self.prac_id}, privilege={self.privilege}, priv_eff_date={self.priv_eff_date}, priv_exp_date={self.priv_exp_date})>"
        )