from sqlalchemy import Column, Integer, String
from models.portico.base import Base


class FmgCities(Base):
    __tablename__ = "fmg_cities"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    ds = Column(String, nullable=True)

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging purposes.
        :return: String representation of the object.
        :rtype: str
        """
        return f"<FmgCities(id={self.id}, ds={self.ds})>"