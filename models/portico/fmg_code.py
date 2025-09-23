from sqlalchemy import Column, String

from models.portico import Base


class FMGCode(Base):
    __tablename__ = "fmg_codes"
    __table_args__ = {"schema": "portown"}

    code = Column(String, primary_key=True)
    TYPE = Column(String, nullable=True, primary_key=True)
    ds = Column(String, nullable=True)