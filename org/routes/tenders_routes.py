
from datetime import date
from fastapi import APIRouter, status, Depends, Path, UploadFile, File, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import Annotated, List, Union

from ..cruds import tenders_cruds
from ..schemas import tenders_schemas
from ..database import get_db
from ..utils.auth import get_superadmin
from ..utils.utils import check_doc_type_file_extension


router = APIRouter(
    prefix="/tenders",
    tags=["Tenders"]
)

@router.get("/{tender_id}", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_200_OK)
async def get_tender(tender_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    db_tender = tenders_cruds.get_tender(db, tender_id)

    return db_tender


@router.get("/", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_200_OK)
async def get_tenders(
    offset: Union[int, None] = 0,
    limit: Union[Annotated[int, Path(le=10)], None] = 10,
    db: Session = Depends(get_db)
):
    db_tenders = tenders_cruds.get_tenders(db, offset, limit)

    return db_tenders


@router.post("/", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_superadmin)])
async def create_tender(
    title: str = Form(...),
    closing_date: date = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    for file in files:
        if not check_doc_type_file_extension(tenders_cruds.get_file_extension(file)): # for ext in extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pdf and csv file formats are allowed."
            )
    
    # Prepare tender data
    tender_data = tenders_schemas.TenderIn(
        tender_title=title,
        tenderClosing_date=closing_date,
        tenderCreated_date=date.today(),
        tenderCreated_by=get_superadmin(),
        tenderUpdated_by=get_superadmin(),
        # Add other fields as needed
    )
    # Create a new tender in the database using the data from tender_in
    new_tender = tenders_cruds.create_single_tender(db=db, tender_in=tender_data)

    for file in files:
        hashed_file = tenders_cruds.hashed_filename(file)
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
            fileCreated_date=date.today(),
            # Add other fields as needed
        )
        tenders_cruds.upload_file(tender_id=new_tender.tender_id, file=file)
        tenders_cruds.create_tender_file(db=db, file=file_info, tender_id=new_tender.tender_id)

    # Return the created tender as response
    return new_tender
    # # Handle file upload
    # # file_path = "storage/files"
    # # filename = tender_file.filename
    # # with open(file_path + "/" + filename, "wb") as f:
    # #     f.write(tender_file.file.read())
    # # new_file = None
    # # if tender_file:
    # update_tender_file = tenders_cruds.hashed_filename(tender_file)
    # # new_file = update_tender_file.filename
    # new_tender = tenders_cruds.create_single_tender(
    #     db=db,
    #     title=title,
    #     closing_date=closing_date,
    #     tender_file=update_tender_file
    # )
    # # if tender_file:
    # #     tenders_cruds.upload_file(tender_id=new_tender.tender_id, file=tender_file)
    # return new_tender
####
# @router.post("/", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_201_CREATED,
#              dependencies=[Depends(get_superadmin)])
# async def create_post(
#     title: str, closing_date: date, tender_file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     file_list = []
#     if tender_file:
#         if tender_file.content_type != "application/pdf":
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid file type. Only PDFs are allowed."
#             )       
#         file_data = await tender_file.read()
#         try:
#             decoded_data = file_data.decode('utf-8')
#         except UnicodeDecodeError:
#             try:
#                 decoded_data = file_data.decode('latin1')
#             except UnicodeDecodeError:
#                 raise HTTPException(
#                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
#                     detail="Unable to decode the byte sequence"
#                 )
#         file_list.append(tenders_schemas.FileCreate(
#             filename=tender_file.filename,
#             filedata=decoded_data,
#             filecreated_date=date.today()
#         ))
#     tender = tenders_schemas.TenderIn(
#         tender_files=file_list, tender_title=title, tenderClosing_date=closing_date,
#         tenderCreated_date=date.today()
#     )
#     db_tender = tenders_cruds.create_tender(
#         db=db, title=title, closing_date=closing_date, tender_file=file_list
#     )
#     return tender


# @router.patch("/{tender_id}", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_201_CREATED,
#               dependencies=[Depends(get_superadmin)])
# async def update_tender(
#     tender_id: Annotated[int, Path(gt=0)], 
#     title: str,
#     closing_date: date,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     tender = tenders_cruds.update_tender(db, tender_id, title, closing_date, files)
#     if not tender:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Tender with id {tender_id} not found."
#         )
#     return tender
####
@router.patch("/{tender_id}", response_model=tenders_schemas.TenderOut, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(get_superadmin)])
async def update_tender(
    tender_id: int,
    title: str = Form(...),
    closing_date: date = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    tender_update = tenders_schemas.TenderUpdate(
        tender_id=tender_id,
        tender_title=title,
        tenderClosing_date=closing_date,
        tenderUpdated_date=date.today()
    )
    
    updated_tender = tenders_cruds.update_tender(db=db, tender_id=tender_id, tender_update=tender_update)

    for file in files: # if files:
        tenders_cruds.add_files_to_tender(db=db, tender_id=tender_id, files=file)

    return updated_tender


@router.delete("/{tender_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
async def delete_tender(tender_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    deleted_tender = tenders_cruds.delete_tender(db, tender_id)

    return deleted_tender