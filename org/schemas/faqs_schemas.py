from fastapi import UploadFile
from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from typing import Union, List
from enum import Enum
from uuid import UUID

class Faq(BaseModel):
    # question: str 
    # answer: str
    # org_id: int
    created_date: datetime
    updated_date: Union[date, None] = None
    
class FAQsIn(Faq):
    question: str
    answer: str
    org_id: int
    
    class Config:
        # from_attributes = True
        from_attributes = True
    
class FAQsOut(Faq):
    id: int
    question: str
    answer: str
    org_id: int
    
    class Config:
        # from_attributes = True
        from_attributes = True