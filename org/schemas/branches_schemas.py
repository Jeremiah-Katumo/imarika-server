
from pydantic import BaseModel
from datetime import datetime, date
from typing import Union


class BranchBase(BaseModel):
    branch_id: int
    branchCreated_date: datetime
    branchUpdated_date: Union[date, None] = None
    branchCreated_by: Union[int, None] = None 
    branchUpdated_by: Union[int, None] = None
    
class BranchCreate(BranchBase):
    branch_name: str
    branch_email: str
    branch_street: str
    branch_address: str
    branch_phone: str
    branch_directions: str

class Branch(BranchBase):
    branch_id: int
    branch_name: str
    branch_email: str
    branch_street: str
    branch_address: str
    branch_phone: str
    branch_directions: str

    class Config:
        # from_attributes = True
        from_attributes = True
        