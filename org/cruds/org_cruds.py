
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date

from ..schemas import org_schemas
from ..models import org_models


def get_all_orgs(db: Session, offset: int, limit: int):
    orgs = db.query(org_models.Org) \
        .order_by(desc(org_models.Org.created_date)) \
            .limit(limit).offset(offset).all()

    if len(orgs) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No Org found"
        )

    return orgs

def get_org(db: Session, org_id: int):
    org = db.query(org_models.Org) \
        .filter(org_models.Org.id == org_id) \
            .first()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Org of id {org_id} not found'
        )
    
    return org

def create_org(db: Session, org: org_schemas.OrgIn):
    existing_org = db.query(org_models.Org) \
        .filter(org_models.Org.name == org.name) \
            .first()
    
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f'Organization with name {org.name} already exists.'
        )

    new_org = org_models.Org(**org.dict(), created_date=date.today())

    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

def update_org(db: Session, org_id: int, org: org_schemas.OrgIn):
    db_org = db.query(org_models.Org) \
        .filter(org_models.Org.id == org_id) \
            .first()

    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Organization with ID {org_id} not found.'
        )

    request_org = org.dict()
    for key, value in request_org.items():
        if value is not None:
            if key == 'core_values' and db_org.core_values:
                setattr(db_org, key, list(set(db_org.core_values + request_org[key])))
            else:
                setattr(db_org, key, value)

    db_org.updated_date = date.today()

    db.commit()
    db.refresh(db_org)

    return db_org

def delete_org(db: Session, org_id: int):
    db_org = db.query(org_models.Org) \
        .filter(org_models.Org.id == org_id) \
            .first()

    if not db_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Organization with ID {org_id} not found.'
        )

    db.delete(db_org)
    db.commit()
    
    return db_org