
import os
import uuid
from datetime import date
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import List

from ...models import org_models
from ...schemas.downloads_schemas import downloadfiles_schemas

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

def upload_file(downloadFile_id: int, file: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if file.size > 100 * 1024 * 1024:  # 100 MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    tender = f"Download_{str(downloadFile_id)}"
    file_path = os.path.join("storage","Downloads","files","download_files",tender)
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

def save_file(
        db: Session, 
        download_file: downloadfiles_schemas.FileCreate
    ) -> org_models.Download:
    # db_file = org_models.Download(filename=file.filename, content=file_data)
    
        
    db_file = org_models.Download(
        downloadFile_title=download_file.downloadFile_title,
        downloadFile_name=download_file.downloadFile_name,
        downloadFile_data=download_file.downloadFile_data,
        downloadFile_category=download_file.downloadFile_category,
        downloadFileCreated_date=date.today(),
        downloadFileUpdated_date=download_file.downloadFileUpdated_date,
        # downloadFileCreated_by=download_file.downloadFileCreated_by,
        # downloadFileUpdated_by=download_file.downloadFileUpdated_by
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file

def update_file(
        db: Session, 
        downloadFile_id: int, 
        download_file: downloadfiles_schemas.FileUpdate
    ) -> org_models.Download:
    db_file = db.query(org_models.Download) \
        .filter(org_models.Download.downloadFile_id == downloadFile_id) \
                .first()

    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"File with id '{downloadFile_id}' not found"
        )
    
    if download_file.downloadFile_title is not None:
        db_file.downloadFile_title = download_file.downloadFile_title
    if download_file.downloadFile_category is not None:
        db_file.downloadFile_category = download_file.downloadFile_category

    db.commit()
    db.refresh(db_file)

    return db_file

async def add_files_to_tender(
        db: Session,
        downloadFile_id: int,
        files: List[UploadFile], 
        download_file: downloadfiles_schemas.FileUpdate
    ):
    db_download_file = db.query(org_models.Download) \
        .filter(org_models.Download.downloadFile_id == downloadFile_id) \
            .first()
    if not db_download_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"File with id '{downloadFile_id}' not found"
        )
    
    for file in files:
        file = hashed_filename(file)
        new_file = file.filename

        file_data = await file.read()
        try:
            decoded_data = file_data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                decoded_data = file_data.decode('latin1')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"File could not be decoded"
                )
            
        file_info = downloadfiles_schemas.FileUpdate(
            downloadFile_id=downloadFile_id,
            downloadFile_title=download_file.downloadFile_title,
            downloadFile_name=new_file,
            downloadFile_data=decoded_data,
            downloadFile_category=download_file.downloadFile_category,
            downloadFileCreated_date=date.today()
        )
            
        upload_file(downloadFile_id=db_download_file.downloadFile_id, file=file)
        save_file(db=db, ddownload_file=file_info)
        # db_download_file.downloadFile_data.append(db_file)


def delete_file(db: Session, filename: str, category: downloadfiles_schemas.DownloadFileCategory):
    db_file = db.query(org_models.Download) \
        .filter(org_models.Download.downloadFile_name == filename) \
            .filter(org_models.Download.downloadFile_category == category) \
                .first()

    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"File '{filename}' not found"
        )

    db.delete(db_file)
    db.commit()

    return db_file

def get_file(db: Session, downloadFile_id: int, category: str):
    db_file = db.query(org_models.Download) \
        .filter(org_models.Download.downloadFile_id == downloadFile_id) \
            .filter(org_models.Download.downloadFile_category == category) \
                .first()

    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"File '{downloadFile_id}' not found"
        )
    
    return db_file
