
from datetime import date
from fastapi import status, HTTPException
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..schemas import contact_schemas
from ..models import org_models


def create_message(db: Session, message: contact_schemas.ContactMessageIn):
    new_message = message.dict()

    org = db.query(org_models.Org) \
        .filter(org_models.Org.id == message.org_id) \
            .first() # .one() also works
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Org of id {message.org_id} not found'
        )

    db_message = org_models.ContactMessage(**new_message)
    # new_message['created_date'] = date.today()
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


def get_messages(db, org_id: int, status_choice: str, offset: int, limit: int):
    
    messages = []

    if status_choice.value == 'All':
        messages = db.query(org_models.ContactMessage) \
            .filter(org_models.ContactMessage.org_id == org_id) \
                .order_by(desc(org_models.ContactMessage.created_date)) \
                    .limit(limit).offset(offset).all()
    else:
        messages = db.query(org_models.ContactMessage) \
            .filter(org_models.ContactMessage.status == status_choice.value) \
                .filter(org_models.ContactMessage.org_id == org_id) \
                    .order_by(desc(org_models.ContactMessage.created_date)) \
                        .limit(limit).offset(offset).all()
    
    if len(messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No {status_choice.value} message found for org Id {org_id}"
        )

    return messages


def get_single_message(db: Session, org_id: int, message_id: int):
    message = db.query(org_models.ContactMessage) \
        .filter(org_models.ContactMessage.id == message_id) \
            .filter(org_models.ContactMessage.org_id == org_id) \
                .first() # .one() also works

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Message of id {message_id} in Org Id {org_id} not found'
        )
    
    return message


def update_message(db: Session, org_id: int, message_id: int, message: contact_schemas.ContactMessageIn):
    request_message = message.dict()
    new_message = db.query(org_models.ContactMessage) \
        .filter(org_models.ContactMessage.id == message_id) \
            .filter(org_models.Org.id == org_id) \
                .first()

    if new_message == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Message of id {message_id} not found'
        )
        
    for key, value in request_message.items():
        if value is not None:
            if key == 'messages' and new_message.messages is not None:
                setattr(new_message, key, list(set(value + new_message.messages)))

    new_message.org_id = org_id
    new_message.updated_date = date.today()

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update the Contact Message due to a foreign key constraint."
        )
    
    # Refresh the instance to get the updated data
    db.refresh(new_message)
    
    return new_message

def delete_message(db: Session, org_id: int, message_id: int):
    delete_message = db.query(org_models.ContactMessage) \
        .filter(org_models.ContactMessage.id == message_id) \
            .filter(org_models.Org.id == org_id) \
                .first()
    
    if delete_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact message of id {message_id} not found"
        )
    
    db.delete(delete_message)
    db.commit()

    return {
        "detail": f"Contact message of id {message_id} from org of id {org_id} not found"
    }
