from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.portico.base import Base

class PPPhones(Base):
    """
    Represents the "pp_phones" table within the "portown" schema.

    This class is a mapped representation of the database table used for
    storing phone information. Each record in this table contains
    attributes such as the phone type, area code, exchange, and number.
    It also establishes a relationship with the `PPAddrPhones` entities for
    mapping associated address information to specific phone records.

    :ivar id: The unique identifier for a phone record.
    :type id: Integer
    :ivar type: The type or category of phone (e.g., mobile, home, work).
    :type type: String
    :ivar area_code: The area code associated with the phone number.
    :type area_code: String
    :ivar exchange: The exchange code for the phone number.
    :type exchange: String
    :ivar number: The specific phone number.
    :type number: String
    :ivar addresses: The relationship to the `PPAddrPhones` table that
        maps phone records to addresses.
    :type addresses: list of PPAddrPhones
    """
    __tablename__ = "pp_phones"
    __table_args__ = {'schema': 'portown'}

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    area_code = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    number = Column(String, nullable=False)

    addresses = relationship('PPAddrPhones', back_populates='phone')

    def __repr__(self):
        """
        Provides a string representation of the `PPPhones` object for debugging and
        logging purposes. The returned string contains details about the `id`,
        `type`, `area_code`, `exchange`, and `number` attributes of the object.

        :return: A string representation of the `PPPhones` object
        :rtype: str
        """
        return (f"<PPPhones(id={self.id}, "
                f"type={self.type}, "
                f"area_code={self.area_code}, "
                f"exchange={self.exchange}, "
                f"number={self.number})>")