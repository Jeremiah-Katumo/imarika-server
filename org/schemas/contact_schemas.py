from datetime import datetime, date
from pydantic import BaseModel
from typing import Union
from enum import Enum

class MessageStatus(str, Enum):
    all = "All"
    new = "New"
    replied = "Replied"

class ContactMessageBase(BaseModel):
    status: Union[str, None] = None
    created_date: datetime
    updated_date: Union[date, None] = None
    created_by: Union[int, None] = None
    updated_by: Union[int, None] = None


class ContactMessageIn(ContactMessageBase):
    name: str 
    org_id: int
    subject: str 
    message: str

    class Config:
        orm_mode=True


class ContactMessageOut(ContactMessageBase):
    id: int
    name: str 
    org_id: int
    subject: str 
    message: str

    class Config:
        orm_mode = True
    