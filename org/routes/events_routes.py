
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..cruds import events_cruds
from ..schemas import events_schemas
from ..database import get_db
from ..utils.auth import get_superadmin

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("/", response_model=events_schemas.Event, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_superadmin)])
def create_event(event: events_schemas.EventCreate, db: Session = Depends(get_db)):
    event = events_cruds.create_event(db=db, event=event)

    return event

@router.get("/{event_id}", response_model=events_schemas.Event, status_code=status.HTTP_200_OK)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = events_cruds.get_event(db, event_id=event_id)
    
    return db_event

@router.get("/", response_model=List[events_schemas.Event], status_code=status.HTTP_200_OK)
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = events_cruds.get_events(db, skip=skip, limit=limit)

    return events

@router.patch("/{event_id}", response_model=events_schemas.Event, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(get_superadmin)])
def update_event(event_id: int, event: events_schemas.EventUpdate, db: Session = Depends(get_db)):
    db_event = events_cruds.update_event(db, event_id=event_id, event=event)
    
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = events_cruds.delete_event(db, event_id=event_id)
    
    return db_event
