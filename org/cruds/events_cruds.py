
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models import org_models
from ..schemas import events_schemas

def get_event(db: Session, event_id: int):
    event = db.query(org_models.Event) \
        .filter(org_models.Event.event_id == event_id) \
            .first()
    
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No event with id {event_id} found"
        )
    
    return event

def get_events(db: Session, skip: int = 0, limit: int = 10) -> List[org_models.Event]:
    events = db.query(org_models.Event) \
        .offset(skip).limit(limit).all()
    
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event found"
        )
    
    return events

def create_event(db: Session, event: events_schemas.EventCreate) -> org_models.Event:
    event_exist = db.query(org_models.Event) \
        .filter(org_models.Event.event_name == event.event_name) \
            .first()
    
    if event_exist is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event already exists"
        )

    db_event = org_models.Event(
        name=event.event_name, 
        date=event.event_date, 
        description=event.event_description
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event

def update_event(db: Session, event_id: int, event: events_schemas.EventUpdate) -> org_models.Event:
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    
    update_data = event.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)

    return db_event

def delete_event(db: Session, event_id: int):
    db_event = get_event(db, event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    
    db.delete(db_event)
    db.commit()

    return db_event
