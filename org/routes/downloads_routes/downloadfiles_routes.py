
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date
import logging
import io

from ...cruds.downloads_cruds import downloadfiles_cruds
from ...schemas.downloads_schemas import downloadfiles_schemas
from ...database import get_db
from ...utils.auth import get_superadmin

router = APIRouter(
    prefix="/downloads",
    tags=['Downloads']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=downloadfiles_schemas.File, 
             dependencies=[Depends(get_superadmin)])
async def upload_file(
    category: downloadfiles_schemas.DownloadFileCategory, 
    title: str = Form(...),
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)
    ):
    for file in files:
        hashed_file = downloadfiles_cruds.hashed_filename(file)
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

    download_file_data = downloadfiles_schemas.FileCreate(
        downloadFile_title=title,
        downloadFile_name=new_file,
        downloadFile_data=decoded_data,
        downloadFile_category=category,
        downloadFileCreated_date=date.today(),
        # downloadFileCreated_by=get_superadmin(),
        # downloadFileUpdated_by=get_superadmin()
    )

    new_download = downloadfiles_cruds.save_file(db=db, download_file=download_file_data)
    downloadfiles_cruds.upload_file(downloadFile_id=new_download.downloadFile_id, file=file)
    
    return new_download

@router.patch("/{filename}", status_code=status.HTTP_201_CREATED, 
              response_model=downloadfiles_schemas.File, dependencies=[Depends(get_superadmin)])
async def update_file( 
    category: downloadfiles_schemas.DownloadFileCategory, 
    downloadFile_id: int,
    title: str = Form(...),
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)
    ):
    for file in files:
        hashed_file = downloadfiles_cruds.hashed_filename(file)
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
            
    download_file_update = downloadfiles_schemas.FileUpdate(
        downloadFile_id=downloadFile_id,
        downloadFile_title=title,
        downloadFile_name=new_file,
        downloadFileUpdated_date=date.today(),
        downloadFile_category=category,
        downloadFile_data=decoded_data
        # downloadFileUpdated_by=get_superadmin()
    )

    db_file = downloadfiles_cruds.update_file(
        db=db, downloadFile_id=downloadFile_id, download_file=download_file_update)

    return db_file

@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
async def delete_file(
    filename: str, 
    category: downloadfiles_schemas.DownloadFileCategory, 
    db: Session = Depends(get_db)
    ):

    db_file = downloadfiles_cruds.delete_file(db, filename, category)

    return {"info": f"file '{filename}' deleted"}

@router.get("/{downloadFile_id}", status_code=status.HTTP_200_OK, response_class=StreamingResponse)
async def download_file(
    category: downloadfiles_schemas.DownloadFileCategory, 
    downloadFile_id: int = Path(..., description="Insert download file id"), 
    db: Session = Depends(get_db)
    ):

    db_file = downloadfiles_cruds.get_file(db, downloadFile_id, category)

    if db_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"File with id '{downloadFile_id}' not found"
        )
    
    # Ensure file data is not empty
    if not db_file.downloadFile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="File data is empty"
        )
    
    # Log file data length for debugging
    logging.debug(f"File Data Length: {len(db_file.downloadFile_data)}")

    # Decode 'latin1' encoded data to bytes
    file_bytes = db_file.downloadFile_data.decode('latin1')

    return StreamingResponse(
        io.BytesIO(file_bytes.encode()), 
        media_type='application/pdf', 
        headers={"Content-Disposition": f"attachment; filename={db_file.downloadFile_name}"}
    )
