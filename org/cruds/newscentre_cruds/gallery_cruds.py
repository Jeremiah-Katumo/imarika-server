
import os
import logging
import hashlib
from fastapi import UploadFile, HTTPException, status, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ...models import org_models
from ...schemas.newscentre_schemas import gallery_schemas


UPLOAD_DIR = "storage/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def hash_file_contents(file: UploadFile) -> str:
    hasher = hashlib.sha256()

    content = file.file.read()

    hasher.update(content)

    file.file.seek(0)  # Reset file pointer after reading

    return hasher.hexdigest()

def get_image(db: Session, image_id: int):
    image = db.query(org_models.Image) \
        .filter(org_models.Image.id == image_id) \
            .first()
    
    return image

def get_images(db: Session, skip: int = 0, limit: int = 10):
    images = db.query(org_models.Image) \
        .offset(skip).limit(limit).all()
    
    return images

def create_image(db: Session, image: gallery_schemas.ImageCreate, filename: str):
    existing_image = db.query(org_models.Image) \
        .filter(org_models.Image.filename == filename) \
            .first()
    
    if existing_image:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Image already exists"
        )
    
    db_image = org_models.Image(**image.dict(), filename=filename)

    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image

def update_image(db: Session, image_id: int, image_data: gallery_schemas.ImageUpdate, file: UploadFile = File(...)):
    # db_image = get_image(db, image_id)
    db_image = db.query(org_models.Image) \
        .filter(org_models.Image.id == image_id).first()
    
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Image with {image_id} not found"
        )
    
    # Update the metadata
    if image_data.title:
        db_image.title = image_data.title
    if image_data.filename:
        db_image.filename = image_data.filename

    # Handle the file upload
    if file:
        try:
            file_extension = file.filename.split('.')[-1]
            file_hash = hash_file_contents(file)
            filename = f"{file_hash}.{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, filename)  # Ensure the directory exists
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            # db_image.url = file_location  # Assuming 'url' is the field storing the file path
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return None
    
    try:
        db.commit()
        db.refresh(db_image)
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        db.rollback()
        return None
    
    return db_image


def delete_image(db: Session, image_id: int):
    db_image = db.query(org_models.Image) \
        .filter(org_models.Image.id == image_id) \
            .first()
    
    if db_image:
        db.delete(db_image)
        db.commit()
        
    return db_image
