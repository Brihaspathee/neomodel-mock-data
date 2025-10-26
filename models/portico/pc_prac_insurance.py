from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from models.portico import Base


class PPPracInsurance(Base):
    __tablename__ = "pc_prac_insurance"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    prac_id = Column(Integer, ForeignKey("portown.pp_prac.id"))
    carrier = Column(String, nullable=True)
    policy = Column(String, nullable=True)
    expires = Column(Date, nullable=True)
    coverage = Column(String, nullable=True)
    effective = Column(Date, nullable=True)
    coverage_type = Column(String, nullable=True)
    coverage_unlimited = Column(String, nullable=True)

    practitioner = relationship("PPPrac", back_populates="insurances")

    def __repr__(self):
        return (f"<PPPracInsurance(id={self.id}, "
                f"prac_id={self.prac_id}, "
                f"carrier={self.carrier}, "
                f"policy={self.policy}, "
                f"expires={self.expires}, "
                f"coverage={self.coverage}, "
                f"effective={self.effective}, "
                f"coverage_type={self.coverage_type}, "
                f"coverage_unlimited={self.coverage_unlimited})>")
