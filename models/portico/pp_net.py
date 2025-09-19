from typing import TypedDict, Optional, List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.portico.base import Base

if TYPE_CHECKING:
    from models.portico.pp_net_attrib import PPNetAttrib, PPNetAttribDict


class PPNetDict(TypedDict, total=False):
    id: str | None
    name: str
    description: str
    level: int
    children: list["PPNetDict"] | None
    attributes: list["PPNetAttribDict"] | None


class PPNet(Base):

    __tablename__ = "pp_net"
    __table_args__ = {"schema": "portown"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column("ds", String, nullable=False) # maps ds -> to name
    description: Mapped[str] = mapped_column("dsl", String, nullable=True) # maps dsl -> to description
    level: Mapped[int] = mapped_column("net_level_id", Integer, nullable=False) # maps net_level_id -> to level

    parent_net_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("portown.pp_net.id"),
        nullable=True
    )

    # self-referential relationship
    parent: Mapped["PPNet"] = relationship(
        "PPNet",
        remote_side=[id],
        back_populates="children",
        uselist=False
    )

    children: Mapped[list["PPNet"]] = relationship(
        "PPNet",
        back_populates="parent",
        lazy="selectin" # eager load optimization
    )

    attributes: Mapped[List["PPNetAttrib"]] = relationship("PPNetAttrib", back_populates="net")

    def to_dict(self, include_children:bool = True) -> PPNetDict:
        data: PPNetDict = {
            "id": str(self.id) if self.id is not None else None,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "attributes": [attrib.to_dict() for attrib in self.attributes]
        }

        if include_children:
            data["children"] = [child.to_dict(include_children=False) for child in self.children]
        return data



    def __repr__(self):
        """
        Provides a string representation of the PPNet object, including its
        """
        return (f"<PPNet(id={self.id}, name={self.name}, "
                f"description={self.description}, level={self.level})>")