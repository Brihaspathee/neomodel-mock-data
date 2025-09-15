from sqlalchemy import Column, Integer, String
from models.portico.base import Base


class FmgCounties(Base):
    __tablename__ = "fmg_counties"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    ds = Column(String, nullable=True)

    def __repr__(self):
        return f"<FmgCounties(id={self.id}, ds={self.ds})>"