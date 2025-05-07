
from pydantic import BaseModel
from datetime import datetime, date
from typing import Union, List, Optional


class FileCreate(BaseModel):
    fileName: str
    fileData: bytes
    fileCreated_date: datetime
    fileUpdated_date: Union[date, None] = None
    fileCreated_by: Union[int, None] = None 
    fileUpdated_by: Union[int, None] = None

class TenderBase(BaseModel):
    tenderCreated_date: datetime
    tenderClosing_date: date
    tenderUpdated_date: Union[date, None] = None
    tenderCreated_by: Union[int, None] = None
    tenderUpdated_by: Union[int, None] = None

class TenderIn(TenderBase):
    tender_title: str
    tender_files: Optional[List[FileCreate]] = []

class TenderOut(TenderBase):
    tender_id: int
    tender_title: str
    tender_files: List[FileCreate]

    class Config:
        from_attributes = True

class TenderUpdate(BaseModel):
    tender_id: int
    tender_title: str
    tender_files: Optional[List[FileCreate]] = []
    tenderClosing_date: Optional[date] = None
    tenderUpdated_date: Optional[datetime] = None
    tenderUpdated_by: Optional[int] = None