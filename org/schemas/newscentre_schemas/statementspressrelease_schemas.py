
from pydantic import BaseModel, validator
from enum import Enum
from datetime import datetime, date
from typing import Union

### THIS SCHEMA IS USED BY DOWNLOADS, AND STATEMENTS AND PRESS RELEASE
class DownloadFileCategory(str, Enum):
    knowledge_base = "Knowledge Base"
    most_used_forms = "Most Used Forms"
    loan_application_forms = "Loans Application Forms"
    savings_accounts_forms = "Savings Application Forms"
    other_documents = "Other Documents"


class FileBase(BaseModel):
    # downloadFile_id: int
    downloadFile_name: str
    downloadFile_title: str
    downloadFile_category: str
    downloadFileCreated_date: datetime
    downloadFileUpdated_date: Union[date, None] = None
    # downloadFileCreated_by: int
    # downloadFileUpdated_by: int


class FileCreate(FileBase):
    downloadFile_data: bytes

    class Config:
        orm_mode = True

    # @validator('downloadFile_data')
    # def check_file_size(cls, value):
    #     max_size = 1024 * 1024 * 10  # 10 MB size limit
    #     if len(value) > max_size:
    #         raise ValueError(f'File size exceeds the maximum limit of {max_size} bytes')
    #     return value
    

class FileResponse(BaseModel):
    info: str


class File(FileBase):
    downloadFile_id: int
    downloadFile_data: bytes

    class Config:
        orm_mode = True

class FileUpdate(BaseModel):
    downloadFile_id: int
    downloadFile_title: str
    downloadFile_name: str
    downloadFile_data: bytes
    downloadFile_category: str
    downloadFileUpdated_date: Union[date, None] = None