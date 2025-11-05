from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from models import Event, Club
from api.schemas.events import *
from datetime import datetime

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == event.club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    
    new_event = Event(
        club_id=event.club_id,
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        location=event.location,
        date=event.date,
        deadline=event.deadline,
        max_seats=event.max_seats,
        is_trending=event.is_trending
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    return new_event


@router.get("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    event.view_count += 1
    db.commit()
    
    return event


@router.put("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventResponse)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(event, field, value)
    
    event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(event)
    
    return event


@router.delete("/{event_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(event)
    db.commit()
    
    return DeleteResponse(
        success=True,
        message="Event deleted successfully",
        timestamp=datetime.utcnow()
    )


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [{
        "id": e.id,
        "title": e.title,
        "club_id": e.club_id,
        "event_type": e.event_type,
        "date": e.date,
        "location": e.location,
        "current_registrations": e.current_registrations
    } for e in events]


@router.get("/club/{club_id}", status_code=status.HTTP_200_OK)
def get_club_events(club_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    
    events = db.query(Event).filter(Event.club_id == club_id).all()
    return [{
        "id": e.id,
        "title": e.title,
        "event_type": e.event_type,
        "date": e.date,
        "location": e.location,
        "current_registrations": e.current_registrations
    } for e in events]


