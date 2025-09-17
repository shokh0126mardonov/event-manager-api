import enum
from sqlalchemy import (
    Column,
    String,
    CheckConstraint,
    Enum,
    Text,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from .base import BaseModel


class EventTypes(str, enum.Enum):
    CONSERT = "consert"
    WEDDING = "wedding"
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    SEMINAR = "seminar"
    OTHER = "OTHER"


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ONGING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Events(BaseModel):
    __tablename__ = "events"

    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    event_type = Column(Enum(EventTypes), default=EventTypes.OTHER, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.DRAFT, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    address = Column(String(256))

    venue_id = Column(Integer, ForeignKey('venues.id'))
    organizer_id = Column(Integer, ForeignKey('users.id'))

    venue = relationship("Venues", back_populates="events")
    organizer = relationship("Users", back_populates="events")
    tickets = relationship("Tickets", back_populates="event")

    __table_args__ = (
        CheckConstraint("char_length(name) >= 3", name="event_name_min_length"),
    )

