from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPProvType(Base):
    __tablename__ = 'pp_prov_type'
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type_ds = Column(String, nullable=False)
    category = Column(String, nullable=False)

    # providers = relationship("PPProv", back_populates="prov_type")

    def __repr__(self):
        """
        Provides a string representation of the PPProvType object.

        This method returns a string that includes the attributes of the object
        in a key-value pair format. It helps in debugging to easily identify
        the current state of the object.

        :return: A string representation of the PPProvType object containing
            its id, type, and category attributes.
        :rtype: str
        """
        return (f"<PPProvType(id={self.id}, "
                f"type={self.type_ds}, "
                f"category={self.category})>")