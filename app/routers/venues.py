from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..models.venues import Venues
from ..schemas.venues import VenueCreate, VenueOut, VenueTypes


router = APIRouter(
    prefix="/venues",
    tags=["Venues"]
)

@router.get("/")
async def get_venues(db: Session = Depends(get_db)):
    venues = db.query(Venues).all()
    return [VenueOut.from_orm(venue) for venue in venues]


@router.post("/", response_model=VenueOut)
async def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    db_venue = Venues(
        name=venue.name,
        location=venue.location,
        venue_type=venue.venue_type,
    )
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)

    return VenueOut.from_orm(db_venue)

@router.get("/{venue_id}", response_model=VenueOut)
async def get_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(Venues).filter(Venues.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return VenueOut.from_orm(venue)

@router.put("/{venue_id}", response_model=VenueOut)
async def update_venue(venue_id: int, updated_venue: VenueCreate, db: Session = Depends(get_db)):
    venue = db.query(Venues).filter(Venues.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )

    venue.name = updated_venue.name
    venue.location = updated_venue.location
    venue.venue_type = updated_venue.venue_type

    db.commit()
    db.refresh(venue)
    return VenueOut.from_orm(venue)

@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(Venues).filter(Venues.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )

    db.delete(venue)
    db.commit()
    return None

