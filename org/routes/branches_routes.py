
from fastapi import APIRouter, status, Path, Depends
from typing import Annotated, Union

from ..schemas import branches_schemas
from ..cruds import branches_cruds
from ..database import db_session
from ..utils.auth import get_superadmin


router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)


@router.get("/{branch_id}", response_model=branches_schemas.Branch, status_code=status.HTTP_200_OK)
async def get_branch(db: db_session, branch_id: Annotated[int, Path(gt=0)]):
    branch = branches_cruds.get_branch(db, branch_id)

    return branch


@router.get("/", response_model=branches_schemas.Branch, status_code=status.HTTP_200_OK)
async def get_branches(
    db: db_session, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10,
    offset: Union[int, None] = 0
):
    branches = branches_cruds.get_branches(db, offset, limit)

    return branches


@router.post("/", response_model=branches_schemas.Branch, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_superadmin)])
async def create_branch(db: db_session, branch: branches_schemas.BranchCreate):
    new_branch = branches_cruds.create_branch(db, branch)

    return new_branch


@router.patch("/{branch_id}", response_model=branches_schemas.Branch, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(get_superadmin)])
async def update_branch(
    db: db_session, branch_id: Annotated[int, Path(gt=0)], 
    branch: branches_schemas.BranchCreate
):
    updated_branch = branches_cruds.update_branch(db, branch_id, branch)

    return updated_branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
async def delete_branch(db: db_session, branch_id: Annotated[int, Path(gt=0)]):
    deleted_branch = branches_cruds.delete_branch(db, branch_id)

    return deleted_branch