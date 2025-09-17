from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..models.events import Events
from ..schemas.events import EventOut, EventCreate, EventUpdate


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/")
async def get_events(db: Session = Depends(get_db)):
    events = db.query(Events).all()
    return [EventOut.from_orm(event) for event in events]


@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Events(
        name = event.name,
        description = event.description,
        event_type = event.event_type,
        status = event.status,
        start_date = event.start_date,
        end_date = event.end_date,
        address = event.address,
        venue_id = event.venue_id,
        organizer_id = event.organizer_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return EventOut.from_orm(db_event)


@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return EventOut.from_orm(event)

@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: int, updated_event: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    event.name = updated_event.name
    event.description = updated_event.description
    event.event_type = updated_event.event_type
    event.status = updated_event.status

    db.commit()
    db.refresh(event)
    return EventOut.from_orm(event)

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    db.delete(event)
    db.commit()
    return None

