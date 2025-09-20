from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPAddrPhones(Base):
    """
    Represents the association between addresses and phones in the
    database.

    This class is used to model the many-to-many relationship between
    the `PPAddr` and `PPPhones` tables through a join table. It stores
    the mapping of address IDs to phone IDs, allowing the retrieval of
    associated phone numbers for a specific address and vice versa.

    :ivar id: The primary key of the association table.
    :type id: int
    :ivar address_id: The foreign key referencing the `PPAddr` table.
    :type address_id: int
    :ivar phone_id: The foreign key referencing the `PPPhones` table.
    :type phone_id: int
    :ivar address: The relationship to the `PPAddr` model.
    :type address: PPAddr
    :ivar phone: The relationship to the `PPPhones` model.
    :type phone: PPPhones
    """
    __tablename__ = "pp_addr_phones"
    __table_args__ = {'schema': 'portown'}

    # id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('portown.pp_addr.id'), primary_key=True)
    phone_id = Column(Integer, ForeignKey('portown.pp_phones.id'), primary_key=True)

    address = relationship("PPAddr", back_populates="phones")
    phone = relationship("PPPhones", back_populates="addresses")

    def __repr__(self):
        """
        Provides a string representation of the object for debugging and logging purposes.

        :return: A string that includes the id, address_id, and phone_id properties of the object.
        :rtype: str
        """
        return (f"<PPAddrPhones( "
                f"address_id={self.address_id}, "
                f"phone_id={self.phone_id})>")
