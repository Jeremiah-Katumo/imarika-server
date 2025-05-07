
from fastapi import status, Path, APIRouter, Depends
from typing import Annotated, Union
from typing import Annotated, Union, List

from ..schemas import contact_schemas
from ..cruds import contact_cruds
from ..database import db_session
from ..utils.auth import get_current_active_user

router = APIRouter(
    prefix="/messages", 
    tags=['Contact']
)

@router.post("/org_messages", response_model=contact_schemas.ContactMessageOut, 
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
def create_org_message(db: db_session, message: contact_schemas.ContactMessageIn):
    message = contact_cruds.create_message(db, message)

    return message


@router.get("/org_messages", response_model=List[contact_schemas.ContactMessageOut], 
            status_code=status.HTTP_200_OK)
def get_org_messages(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    status: contact_schemas.MessageStatus, 
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10
    ):
    
    messages = contact_cruds.get_messages(db, org_id, status, offset, limit)

    return messages

@router.get("/{message_id}/org_messages/{org_id}", response_model=contact_schemas.ContactMessageOut,
            status_code=status.HTTP_200_OK)
def get_single_message(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    message_id: Annotated[int, Path(gt=0)]
    ):

    message = contact_cruds.get_single_message(db = db, org_id = org_id, message_id = message_id)

    return message

@router.patch("/{message_id}/org_messages/{org_id}", response_model=contact_schemas.ContactMessageOut,
              status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
def update_single_message(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    message_id: Annotated[int, Path(gt=0)], 
    message: contact_schemas.ContactMessageIn
    ):

    message = contact_cruds.update_message(db, org_id, message_id, message)

    return message

@router.delete("/{message_id}/org_messages/{org_id}", status_code=status.HTTP_204_NO_CONTENT, 
               dependencies=[Depends(get_current_active_user)])
def delete_single_message(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    message_id: Annotated[int, Path(gt=0)]
    ):

    message = contact_cruds.delete_message(db, org_id, message_id)

    return message

