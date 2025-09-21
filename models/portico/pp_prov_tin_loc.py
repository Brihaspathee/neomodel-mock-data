from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.portico.base import Base


class PPProvTinLoc(Base):

    __tablename__ = "pp_prov_tin_loc"
    __table_args__ = {"schema": "portown"}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    PRIMARY = Column(String, nullable=False)

    address_id = Column(Integer, ForeignKey("portown.pp_addr.id"))
    address = relationship("PPAddr")

    prov_locs: Mapped[List["PPProvLoc"]] = relationship("PPProvLoc", back_populates="location")

    # providers: Mapped[List["PPProv"]] = relationship(
    #     "PPProv",
    #     secondary="portown.pp_prov_loc"
    # )

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging purposes.
        :return: String representation of the object.
        """
        return (f"<{self.__class__.__name__}(id={self.id}, "
                f"name={self.name}, "
                f"primary={self.PRIMARY})>")