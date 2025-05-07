
from datetime import date
from fastapi import Path, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union, Annotated

from ..models import org_models
from ..schemas import branches_schemas


def get_branches(db: Session, offset: Union[int, None] = 0, limit: Union[Annotated[int, Path(le=10)], None] = 10):
    branches = db.query(org_models.Branch) \
        .order_by(org_models.Branch.branchCreated_date) \
            .limit(limit).offset(offset).all()
    
    if branches is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No branch found"
        )
    
    return branches


def get_branch(db: Session, branch_id: Annotated[int, Path(gt=0)]):
    branch = db.query(org_models.Branch) \
        .filter(org_models.Branch.branch_id == branch_id) \
            .first()
    
    if branch == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch not found"
        )
    
    return branch


def create_branch(db: Session, branch: branches_schemas.BranchCreate):
    new_branch = branch.dict()

    branch = db.query(org_models.Branch) \
        .filter(org_models.Branch.branch_name == branch.branch_name) \
            .first()
    
    if branch != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Branch with name {branch.branch_name} already exists"
        )
    
    new_branch.update({"branchCreated_date": date.today()})
    db_branch = org_models.Branch(**new_branch)

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_branch


def update_branch(db: Session, branch_id: Annotated[int, Path(gt=0)],
                  branch: branches_schemas.BranchCreate):
    req_branch = branch.dict()

    new_branch = db.query(org_models.Branch) \
        .filter(org_models.Branch.branch_id == branch_id).first()
    
    if new_branch == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch with id {branch_id} not found"
        )
    
    for key, value in req_branch.items():
        if value is not None:
            if key == "branches" and new_branch.branches is not None:
                setattr(new_branch, key, list(set(value + new_branch.branches)))
            else:
                setattr(new_branch, key, value)
    
    new_branch.branchUpdated_date = date.today()

    db.commit()
    db.refresh(new_branch)

    return new_branch


def delete_branch(db: Session, branch_id: Annotated[int, Path(gt=0)]):
    branch = db.query(org_models.Branch) \
        .filter(org_models.Branch.branch_id == branch_id).first()
    
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch with id {branch_id} not found"
        )
    
    db.delete(branch)
    db.commit()

    return branch