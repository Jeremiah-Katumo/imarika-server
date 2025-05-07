
import os
from typing import List, Union, Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Path
from sqlalchemy.orm import Session

from ...cruds.newscentre_cruds import gallery_cruds
from ...schemas.newscentre_schemas import gallery_schemas
from ...database import get_db
from ...utils.auth import get_current_active_user

router = APIRouter(
    prefix="/newscentre",
    tags=['News Centre - Gallery']
)

UPLOAD_DIR = "storage/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/images/{image_id}", status_code=status.HTTP_200_OK, 
            response_model=gallery_schemas.ImageOut)
def read_image(image_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    db_image = gallery_cruds.get_image(db, image_id)

    if db_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Image not found"
        )
    
    return db_image

@router.get("/images", status_code=status.HTTP_200_OK,
            response_model=List[gallery_schemas.ImageOut])
def read_images(
    skip: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10, 
    db: Session = Depends(get_db)
    ):
    
    images = gallery_cruds.get_images(db, skip=skip, limit=limit)

    return images

@router.post("/images", response_model=gallery_schemas.ImageOut, 
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
async def create_new_image(title: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format")
    
    file_extension = file.filename.split('.')[-1].lower()

    file_hash = gallery_cruds.hash_file_contents(file)

    filename = f"{file_hash}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    image_create = gallery_schemas.ImageCreate(title=title, filename=filename)

    db_image = gallery_cruds.create_image(db, image_create, filename)

    return db_image

@router.patch("/images/{image_id}", response_model=gallery_schemas.ImageOut, 
              status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
def update_existing_image(
    image_id: Annotated[int, Path(gt=0)],
    title: str = Form(...),
    # filename: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_extension = file.filename.split('.')[-1].lower()

    file_hash = gallery_cruds.hash_file_contents(file)

    filename = f"{file_hash}.{file_extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    image_data = gallery_schemas.ImageUpdate(id=image_id, title=title, filename=filename)
    
    db_image = gallery_cruds.update_image(db, image_id, image_data, file)
    
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found or could not be updated")
    
    return db_image


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_active_user)])
def delete_existing_image(image_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    db_image = gallery_cruds.get_image(db, image_id)

    if db_image:
        file_path = os.path.join(UPLOAD_DIR, db_image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    db_delete_image = gallery_cruds.delete_image(db, image_id)

    return db_delete_image

@router.post("/gallery", response_model=List[gallery_schemas.ImageOut], 
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user)])
async def create_gallery(
    headings: List[str] = Form(...),
    descriptions: List[str] = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
    ):

    if len(headings) != len(descriptions) or len(headings) != len(files):
        raise HTTPException(status_code=400, detail="Mismatched input lengths")
    
    created_images = []
    
    for i in range(len(headings)):
        if files[i].content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        file_extension = files[i].filename.split('.')[-1]

        file_hash = gallery_cruds.hash_file_contents(files[i])

        filename = f"{file_hash}.{file_extension}"

        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(files[i].file.read())

        image_create = gallery_schemas.ImageCreate(title=headings[i])

        created_image = gallery_cruds.create_image(db, image_create, filename)

        created_images.append(created_image)
    
    return created_images
