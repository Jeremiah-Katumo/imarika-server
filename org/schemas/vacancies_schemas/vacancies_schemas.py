
from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Union

class VacancyCategory(str, Enum):
    job = "job"
    internship = "internship"

# JOBS SCHEMAS
class VacancyBase(BaseModel):
    title: str
    description: str
    requirements: str
    duration: date
    reference_number: str
    how_to_apply: str
    created_date: datetime
    updated_date: Union[date, None] = None
    created_by: Union[int, None] = None 
    updated_by: Union[int, None] = None

class VacancyCreate(VacancyBase):
    category: str

class Vacancy(VacancyBase):
    vacancy_id: int
    category: str

    class Config:
        orm_mode = True
