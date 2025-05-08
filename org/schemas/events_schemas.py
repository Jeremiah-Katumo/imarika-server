
from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    event_description: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    event_id: int
    event_name: str = None
    event_date: datetime = None
    event_description: str = None

class Event(EventBase):
    event_id: int

    class Config:
        # from_attributes = True
        from_attributes = True
