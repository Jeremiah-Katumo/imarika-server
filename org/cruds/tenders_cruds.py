
import os
import uuid
from datetime import date, datetime
from fastapi import Path, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import Union, Annotated, List

from ..models import org_models
from ..schemas import tenders_schemas

def create_single_tender(db: Session, tender_in: tenders_schemas.TenderIn) -> org_models.Tender:
    # Create a new Tender instance using the provided data
    db_tender = org_models.Tender(
        tender_title=tender_in.tender_title,
        tenderCreated_date=date.today(),
        tenderClosing_date=tender_in.tenderClosing_date,
        tenderUpdated_date=tender_in.tenderUpdated_date,
        tenderCreated_by=tender_in.tenderCreated_by,
        tenderUpdated_by=tender_in.tenderUpdated_by
    )
    db.add(db_tender)
    db.commit()
    db.refresh(db_tender)
    
    return db_tender

def create_tender_file(db: Session, file: tenders_schemas.FileCreate, tender_id: Annotated[int, Path(gt=0)]) -> org_models.File:
    db_file = org_models.File(
        fileName=file.fileName,
        fileData=file.fileData,
        fileCreated_date=file.fileCreated_date,
        fileUpdated_date=file.fileUpdated_date,
        fileCreated_by=file.fileCreated_by,
        fileUpdated_by=file.fileUpdated_by,
        tender_id=tender_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file



def get_file_extension(file: UploadFile) -> str: # general_schemas.DocTypeFileExtensions:
    # extract filename from the profile_picture
    filename = file.filename
    # split filename using the dot (.) as the delimiter. 
    # The last element of the split result (which is at index -1) represents the file extension.
    file_extension = filename.split('.')[-1].lower()
    return file_extension
    

def hashed_filename(file: UploadFile) -> UploadFile:
    file_hash = uuid.uuid4()
    
    file.filename = f"{file_hash}.{get_file_extension(file)}"

    return file

def upload_file(tender_id: int, file: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if file.size > 100 * 1024 * 1024:  # 100 MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    tender = f"tender_{str(tender_id)}"
    file_path = os.path.join("tenders","files","tender_files",tender)
    # if directory path does not exist create it 
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    # construct the full file path by joining the directory path and the filename of the profile picture
    full_file_path = os.path.join(file_path, file.filename)
    # Checks if a file with the same name already exists in the directory. If it does, it removes the existing file.
    if os.path.exists(full_file_path):
        os.remove(full_file_path)
    # Opens the full file path in write binary mode and writes the contents of the profile picture file to it.
    with open(full_file_path, "wb") as file_pdf:
        file_pdf.write(file.file.read())

    return file.filename


def get_tender(db: Session, tender_id: Annotated[int, Path(gt=0)]):
    tender = db.query(org_models.Tender) \
        .filter(org_models.Tender.tender_id == tender_id).first()
    
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tender with id {tender_id} not found"
        )
    
    return tender


def get_tenders(db: Session, offset: Union[int, None] = 0, limit: Union[Annotated[int, Path(le=10)], None] = 10):
    tenders = db.query(org_models.Tender) \
        .limit(limit).offset(offset).all()
    
    if tenders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tenders found"
        )
    
    return tenders


def update_tender(db: Session, tender_id: int, tender_update: tenders_schemas.TenderIn) -> org_models.Tender:
    db_tender = get_tender(db, tender_id)
    if not db_tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    if tender_update.tender_title is not None:
        db_tender.tender_title = tender_update.tender_title
    
    if tender_update.tenderClosing_date is not None:
        db_tender.tenderClosing_date = tender_update.tenderClosing_date

    db_tender.tenderUpdated_date = datetime.now()
    
    db.commit()
    db.refresh(db_tender)
    return db_tender

async def add_files_to_tender(db: Session, tender_id: int, files: List[UploadFile], 
                              tender: tenders_schemas.FileCreate):
    db_tender = get_tender(db, tender_id)
    if not db_tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Tender not found"
        )
    
    for file in files:
        hashed_file = hashed_filename(file)
        new_file = hashed_file.filename

        file_data = await file.read()
        try:
            decoded_data = file_data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                decoded_data = file_data.decode('latin1')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail="Unable to decode the byte sequence"
                )

        file_info = tenders_schemas.FileCreate(
            fileName=new_file,
            fileData=decoded_data,
            fileCreated_date=datetime.now(),
        )
        
        upload_file(tender_id=db_tender.tender_id, file=file)

        create_tender_file(db=db, file=file_info, tender_id=tender_id)



def delete_tender(db: Session, tender_id: Annotated[int, Path(gt=0)]):
    tender = db.query(org_models.Tender) \
        .filter(org_models.Tender.tender_id == tender_id).first()
    
    if tender == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tender with id {tender_id} not found"
        )
    
    db.delete(tender)
    db.commit()

    return tender
