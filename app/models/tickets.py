import enum
from sqlalchemy import (
    Column,
    Float,
    CheckConstraint,
    Enum,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .base import BaseModel


class TicketTypes(str, enum.Enum):
    VIP = "vip"
    STANDARD = "standard"
    ECONOM = "econom"


class Tickets(BaseModel):
    __tablename__ = "tickets"

    ticket_type = Column(Enum(TicketTypes), default=TicketTypes.ECONOM, nullable=False)
    price = Column(Float)
    quantity = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))

    event = relationship("Events", back_populates="tickets")
