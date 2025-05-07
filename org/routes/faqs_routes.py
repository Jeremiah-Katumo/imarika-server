
from fastapi import status, Path, APIRouter, Depends
from typing import Annotated, List, Union

from ..schemas import faqs_schemas
from ..cruds import faqs_cruds
from ..database import db_session
from ..utils.auth import get_superadmin

 
router = APIRouter(
    prefix="/faqs",
    tags=['FAQs']
)


@router.get("/{faq_id}/org_faqs/{org_id}", status_code=status.HTTP_200_OK, 
            response_model=faqs_schemas.FAQsOut)
def get_all_org_faq_faqs_items(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    faq_id: Annotated[int, Path(gt=0)]
    ):

    faq = faqs_cruds.get_single_org_faq(db, org_id, faq_id)
    
    return faq

@router.get("/org_faqs/{org_id}", status_code=status.HTTP_200_OK, 
            response_model=List[faqs_schemas.FAQsOut])
def get_org_faq_items(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=5)], None] = 5
    ):

    faqs = faqs_cruds.get_org_faq_items(db, org_id, offset, limit)
        
    return faqs

@router.post('/org_faqs/{org_id}', status_code=status.HTTP_201_CREATED, 
             response_model=faqs_schemas.FAQsOut, dependencies=[Depends(get_superadmin)])
def create_org_faq_faq_item(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    faq: faqs_schemas.FAQsIn
    ):

    faq = faqs_cruds.create_faq(db, org_id, faq)
    
    return faq

@router.patch("/{faq_id}/org_faqs/{org_id}", status_code=status.HTTP_201_CREATED, 
              response_model=faqs_schemas.FAQsOut, dependencies=[Depends(get_superadmin)])
def update_org_faq_faq_item(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    faq_id: Annotated[int, Path(gt=0)], 
    faq: faqs_schemas.FAQsIn
    ):

    updated_faq = faqs_cruds.update_faqs(db, org_id, faq_id, faq)
    
    return updated_faq

@router.delete("/{faq_id}/org_faqs/{org_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_superadmin)])
def delete_org_faq_faq_item(
    db: db_session, 
    org_id: Annotated[int, Path(gt=0)], 
    faq_id: Annotated[int, Path(gt=0)]
    ):

    deleted_faq = faqs_cruds.delete_faq(db, org_id, faq_id)

    return deleted_faq
