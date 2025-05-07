
from fastapi import APIRouter, status, Path, Depends
from typing import Annotated, Union, List
from sqlalchemy.orm import Session

from ..schemas import org_schemas, auth_schemas  # Ensure user_schemas is imported
from ..cruds import org_cruds
from ..database import get_db
from ..utils.auth import get_superadmin

router = APIRouter(
    prefix="/org",
    tags=['Organization']
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[org_schemas.OrgOut])
def get_all_orgs(
    db: Session = Depends(get_db), 
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10
    ):

    orgs = org_cruds.get_all_orgs(db, offset, limit)

    return orgs

@router.get("/{org_id}", status_code=status.HTTP_200_OK, response_model=org_schemas.OrgOut)
def get_org(org_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    org = org_cruds.get_org(db, org_id)

    return org

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=org_schemas.OrgOut, 
             dependencies=[Depends(get_superadmin)])
def create_org(org: org_schemas.OrgIn, db: Session = Depends(get_db)):
    new_org = org_cruds.create_org(db, org)

    return new_org

@router.patch("/{org_id}", response_model=org_schemas.OrgOut, status_code=status.HTTP_201_CREATED, 
              dependencies=[Depends(get_superadmin)])
def update_org(
    org_id: Annotated[int, Path(gt=0)], 
    org: org_schemas.OrgIn, 
    db: Session = Depends(get_db)
    ):

    updated_org = org_cruds.update_org(db, org_id, org)

    return updated_org

@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
def delete_org(org_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    delete_org = org_cruds.delete_org(db, org_id)

    return delete_org
