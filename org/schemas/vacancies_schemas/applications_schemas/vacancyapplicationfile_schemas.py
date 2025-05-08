
from pydantic import BaseModel, validator
from typing import List, Union
from enum import Enum
from datetime import date, datetime


class VacancyApplicationCategory(str, Enum):
    job_application = "job application"
    internship_application = "internship application"

class FileCreate(BaseModel):
    fileName: str
    fileData: bytes
    fileCreated_date: datetime
    fileUpdated_date: Union[date, None] = None
    fileCreated_by: Union[int, None] = None 
    fileUpdated_by: Union[int, None] = None

    # @validator('filedata')
    # def check_file_size(cls, value):
    #     max_size = 1024 * 1024 * 10  # 10 MB size limit
    #     if len(value) > max_size:
    #         raise ValueError(f'File size exceeds the maximum limit of {max_size} bytes')
    #     return value

# class File(BaseModel):
#     id: int
#     filename: str

#     class Config:
#         from_attributes = True

class VacancyBase(BaseModel):
    # vacancyApplication_id: int
    vacancyApplicationCreated_date: datetime
    vacancyApplicationUpdated_date: Union[date, None] = None
    vacancyApplicationCreated_by: Union[int, None] = None 
    vacancyApplicationUpdated_by: Union[int, None] = None


class VacancyApplicationCreate(VacancyBase):
    vacancy_id: int
    vacancyApplication_category: str
    vacancyApplication_files: List[FileCreate]

 
class VacancyApplication(VacancyBase):
    vacancy_id: int
    vacancyApplication_id: int
    vacancyApplication_category: str
    vacancyApplication_files: List[FileCreate]

    class Config:
        # from_attributes = True
        from_attributes = True

class VacancyApplicationUpdate(VacancyBase):
    vacancy_id: int
    vacancyApplication_id: int
    vacancyApplication_category: str
    vacancyApplication_files: List[FileCreate]
