
from pydantic import BaseModel
from datetime import date, datetime
from typing import Union


class DepartmentBase(BaseModel):
    # department_id: int
    departmentCreated_date: datetime
    departmentUpdated_date: Union[date, None] = None
    departmentCreated_by: Union[int, None] = None
    departmentUpdated_by: Union[int, None] = None

class DepartmentCreate(DepartmentBase):
    department_title: str
    department_image: Union[str, None] = None

class Department(DepartmentBase):
    department_id: int
    department_title: str
    department_image: Union[str, None] = None

    class Config:
        orm_mode = True