
import os
import uuid
from datetime import date
from fastapi import UploadFile, HTTPException, status, File, Path
from sqlalchemy.orm import Session
from typing import Union, Annotated

from ...models import org_models
from ...schemas import general_schemas
from ...schemas.careers_schemas import departments_schemas
from ...utils.utils import check_image_type_file_extension

def create_single_department(
        db: Session,
        title: str,
        department_image: UploadFile = File(...)
    ) -> departments_schemas.Department:
   
    department_in_db = db.query(org_models.Department) \
            .filter(org_models.Department.department_title == title) \
                .first()

    if department_in_db !=  None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail=f'Department with title {title} already exists'
        )

    department = org_models.Department(
        department_title = title,
        department_image = department_image,
        departmentCreated_date = date.today()
    )
    
    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_image_extension(image: UploadFile) -> str:
    # extract filename from the profile_picture
    image = image.filename
    # split filename using the dot (.) as the delimiter. 
    # The last element of the split result (which is at index -1) represents the file extension.
    image_extension = image.split('.')[-1].lower()

    return image_extension

def hashed_department_image(department_image: UploadFile) -> UploadFile:
    image_hash = uuid.uuid4()
    
    department_image.filename = f"{image_hash}.{get_image_extension(department_image)}"

    return department_image

def upload_file(department_id: int, department_image: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if department_image.size > 2 * 1024 * 1024:  # 2 MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    member = f"department_{str(department_id)}"
    department_image_path = os.path.join("storage","department","images","department_images",member)
    # if directory path does not exist create it 
    if not os.path.exists(department_image_path):
        os.makedirs(department_image_path)
    # construct the full file path by joining the directory path and the filename of the profile picture
    full_image_path = os.path.join(department_image_path, department_image.filename)
    # Checks if a file with the same name already exists in the directory. If it does, it removes the existing file.
    if os.path.exists(full_image_path):
        os.remove(full_image_path)
    # Opens the full file path in write binary mode and writes the contents of the profile picture file to it.
    with open(full_image_path, "wb") as image:
        image.write(department_image.file.read())


def create_department(
    db: Session, title: str, department_image: UploadFile = File(...)
) -> departments_schemas.Department:
    if department_image and not check_image_type_file_extension(get_image_extension(department_image)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only png, jpg and jpeg file formats are allowed."
        )
    
    new_image = None
    if department_image:
        update_department_image = hashed_department_image(department_image)
        new_image = update_department_image.filename

    new_department = create_single_department(
        db=db,
        title=title,
        department_image=new_image
    )

    if department_image:
        upload_file(title, hashed_department_image(department_image))

    return new_department


def get_departments(
    db: Session, offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10
):
    departments = db.query(org_models.Department) \
        .limit(limit).offset(offset).all()
    
    if departments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No departments found."
        )
    
    return departments


def get_department(
    db: Session,
    department_id: Annotated[int, Path(gt=0)]
):
    department = db.query(org_models.Department) \
        .filter(org_models.Department.department_id == department_id).first()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found."
        )
    
    return department


def update_department(
    db: Session,
    department_id: Annotated[int, Path(gt=0)],
    title: str,
    department_image: UploadFile = File(...)
):
    department = db.query(org_models.Department) \
        .filter(org_models.Department.department_id == department_id).first()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found."
        )
    
    if department_image:
        if department_image.size > 2 * 1024 * 1024:  # 2 MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only files of size 2 MB or below are allowed."
            )
        # if not check_image_type_file_extension(get_image_extension(department_id)):
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Only png and jpg file formats are allowed."
        #     )

        department_image = hashed_department_image(department_image)
        department_image_filename = department_image.filename
        upload_file(department_id, department_image)
        department.department_image = department_image_filename

    if title is not None:
        department.department_title = title
    
    db.commit()
    db.refresh(department)

    return department



def delete_department(db: Session, department_id: Annotated[int, Path(gt=0)]):
    department = db.query(org_models.Department) \
        .filter(org_models.Department.department_id == department_id).first()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found."
        )
    
    db.delete(department)
    db.commit()

    return department