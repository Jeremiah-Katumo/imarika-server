
from datetime import date
from fastapi import status, HTTPException
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..schemas import faqs_schemas
from ..models import org_models


def create_faq(db: Session, org_id: int, faq: faqs_schemas.FAQsIn):
    new_faq = faq.dict()

    # check if the question already exists
    faq_in_db = db.query(org_models.Faq) \
        .filter(org_models.Faq.question == faq.question) \
            .filter(org_models.Faq.org_id == org_id) \
                .first()
    
    if faq_in_db != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f'Faq with question "{faq.question}" already exists'
        )
    
    # if the question is not in database, add it
    new_faq.update({'created_date': date.today(), 'org_id': org_id})  
    db_faq = org_models.Faq(**new_faq)

    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    
    return db_faq

def get_single_org_faq(db: Session, org_id: int, faq_id: int):
    faq = db.query(org_models.Faq) \
        .filter(org_models.Faq.org_id == org_id) \
            .filter(org_models.Faq.id == faq_id).first()

    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Faq of id {faq_id} in org {org_id} not found"
        )
            
    return faq

def get_org_faq_items(db: Session, org_id: int, offset: int, limit: int):
    faqs = db.query(org_models.Faq)\
        .filter(org_models.Faq.org_id == org_id)\
            .order_by(desc(org_models.Faq.created_date)) \
                .limit(limit).offset(offset).all()
        
    if not faqs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Faq in org {org_id} is not found'
        )
        
    return faqs

def update_faqs(db: Session, org_id: int, faq_id: int, faq: faqs_schemas.FAQsIn):
    req_faq = faq.dict()
    
    new_faq = db.query(org_models.Faq) \
        .filter(org_models.Faq.id == faq_id) \
            .filter(org_models.Faq.org_id == org_id) \
                .one_or_none()  # Use one_or_none() to avoid exceptions if not found
    
    if new_faq is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Faq of id {faq_id} from Org of id {org_id} not found'
        )
        
    # Update the fields of the FAQ instance
    for key, value in req_faq.items():
        if value is not None:
            if key == 'faqs' and new_faq.faqs is not None:
                setattr(new_faq, key, list(set(value + new_faq.faqs)))
            else:
                setattr(new_faq, key, value)
    
    # Ensure the org_id remains unchanged
    new_faq.org_id = org_id
    
    # Update the updated_date field
    new_faq.updated_date = date.today()
    
    # Commit the transaction to save the changes
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update the FAQ due to a foreign key constraint."
        )
    
    # Refresh the instance to get the updated data
    db.refresh(new_faq)
    
    return new_faq

def delete_faq(db: Session, org_id: int, faq_id: int):
    faq = db.query(org_models.Faq) \
        .filter(org_models.Faq.id == faq_id) \
            .filter(org_models.Org.id == org_id) \
                .first()

    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Faq with ID {faq_id} not found.'
        )
    
    db.delete(faq)
    db.commit()

    return {
        "detail": f"Faq {faq_id} from Organization {org_id} deleted successfuly"
    }
