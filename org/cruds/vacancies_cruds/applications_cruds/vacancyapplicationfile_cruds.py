
import os
import uuid
from datetime import date, datetime
from fastapi import UploadFile, HTTPException, status, File, Path
from sqlalchemy.orm import Session
from typing import Annotated, Union, List

from ....models import org_models
from ....schemas.vacancies_schemas.applications_schemas import vacancyapplicationfile_schemas


def create_single_vacancy_application(
        db: Session, 
        vacancy_application: vacancyapplicationfile_schemas.VacancyApplicationCreate,
        # vacancy_id: Annotated[int, Path(gt=0)],
        category: str,
        # vacancy_application_file: UploadFile = File(...)
    ) -> org_models.VacancyApplication:
   
    db_vacancy_application = org_models.VacancyApplication(
        vacancy_id=vacancy_application.vacancy_id,
        vacancyApplication_category=category,
        vacancyApplicationCreated_date=date.today(),
        vacancyApplicationUpdated_date=vacancy_application.vacancyApplicationUpdated_date,
        vacancyApplicationCreated_by=vacancy_application.vacancyApplicationCreated_by,
        vacancyApplicationUpdated_by=vacancy_application.vacancyApplicationUpdated_by
    )

    db.add(db_vacancy_application)
    db.commit()
    db.refresh(db_vacancy_application)

    return db_vacancy_application


def create_vacancy_application_file(
    db: Session, 
    file: vacancyapplicationfile_schemas.FileCreate,
    vacancyApplication_id: Annotated[int, Path(gt=0)],
    ) -> org_models.File:
    db_file = org_models.File(
        fileName=file.fileName,
        fileData=file.fileData,
        fileCreated_date=file.fileCreated_date,
        fileUpdated_date=file.fileUpdated_date,
        fileCreated_by=file.fileCreated_by,
        fileUpdated_by=file.fileUpdated_by,
        vacancyApplication_id=vacancyApplication_id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file

def get_file_extension(file: UploadFile) -> str:
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

def upload_file(vacancy_id: int, vacancy_application_id: int, file: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if file.size > 100 * 1024 * 1024:  # 100 MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    vacancy = f"vacancy_{str(vacancy_id)}"
    vacancy_application = f"vacancy_application_{str(vacancy_application_id)}"
    file_path = os.path.join("storage","Vacancy_application","files","vacancy_application_files",vacancy,vacancy_application)
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


def get_vacancy_application(
    db: Session, 
    vacancy_id: Annotated[int, Path(gt=0)],
    application_id: Annotated[int, Path(gt=0)], 
    category: str
):
    vacancy_application = db.query(org_models.VacancyApplication) \
        .filter(org_models.VacancyApplication.vacancyApplication_id == application_id) \
            .filter(org_models.VacancyApplication.vacancy_id == vacancy_id) \
                .filter(org_models.VacancyApplication.vacancyApplication_category == category) \
                    .first()
    
    return vacancy_application


def get_vacancy_applications(
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory, 
    db: Session, offset: Union[int, None] = 0, limit: Union[Annotated[int, Path(le=10)], None] = 10
):
    vacancy_applications = db.query(org_models.VacancyApplication) \
        .filter(org_models.VacancyApplication.vacancyApplication_category == category) \
            .limit(limit).offset(offset).all()

    return vacancy_applications

### I DON'T THINK UPDATE IS REQUIRED IN APPLICATIONS
def update_vacancy_application(
    db: Session,
    vacancy_id: Annotated[int, Path(gt=0)],
    vacancy_application_id: Annotated[int, Path(gt=0)],
    category: str,
    vacancy_application_update: vacancyapplicationfile_schemas.VacancyApplicationCreate
):
    db_vacancy_application = get_vacancy_application(db, vacancy_id, vacancy_application_id, category)
    if not db_vacancy_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy Application not found"
        )
    
    if vacancy_application_update.vacancyApplication_category is not None:
        db_vacancy_application.vacancyApplication_category = vacancy_application_update.vacancyApplication_category

    db_vacancy_application.vacancyApplicationUpdated_date = datetime.now()

    db.commit()
    db.refresh(db_vacancy_application)

    return db_vacancy_application

async def add_files_to_vacancy_application(
        db: Session, vacancy_id: int, vacancy_application_id: int, category: str,
        files: List[UploadFile], vacancy_application: vacancyapplicationfile_schemas.FileCreate
    ):
    db_vacancy_application = get_vacancy_application(db, vacancy_id, vacancy_application_id, category)
    if not db_vacancy_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Vacancy application not found"
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

        file_info = vacancyapplicationfile_schemas.FileCreate(
            fileName=new_file,
            fileData=decoded_data,
            fileCreated_date=datetime.now(),
        )
        
        upload_file(tender_id=db_vacancy_application.tender_id, file=file)

        create_vacancy_application_file(db=db, file=file_info, vacancyApplication_id=vacancy_application_id)


### I DON'T THINK DELETE IS REQUIRED IN APPLICATIONS
def delete_vacancy_application(
    db: Session,
    vacancy_id: Annotated[int, Path(gt=0)],
    application_id: Annotated[int, Path(gt=0)],
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory,
):
    vacancy_application = db.query(org_models.VacancyApplication) \
        .filter(org_models.VacancyApplication.vacancyApplication_category == category) \
            .filter(org_models.VacancyApplication.vacancyApplication_id == application_id) \
                .filter(org_models.VacancyApplication.vacancy_id == vacancy_id) \
                    .first()
    
    if not vacancy_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vacancy application with id {application_id} not found."
        )
    
    return vacancy_application
