
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Path
from sqlalchemy.orm import Session
from typing import List, Union, Annotated

from ....schemas.vacancies_schemas.applications_schemas import vacancyapplicationfile_schemas
from ....cruds.vacancies_cruds.applications_cruds import vacancyapplicationfile_cruds
from ....database import get_db
from ....utils.auth import get_current_active_user, get_superadmin
from ....utils.utils import check_doc_type_file_extension


router = APIRouter(
    prefix="/applications",
    tags=['Vacancies - Applications']
)

@router.post("/vacancies/{vacancy_id}", response_model=vacancyapplicationfile_schemas.VacancyApplication,
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_user), Depends(get_superadmin)])
async def apply_for_vacancy(
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory,
    vacancy_id: int = Path(..., description="The ID of the vacancy"), 
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)
):
    file_list = []

    for file in files:
        if not check_doc_type_file_extension(vacancyapplicationfile_cruds.get_file_extension(file)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid file type. Only PDFs and CSVs are allowed."
            )
        
        hashed_file = vacancyapplicationfile_cruds.hashed_filename(file)
        new_file = hashed_file.filename
        file_data = await file.read()

        # Decoding the byte data using UTF-8 encoding first, then fallback to latin1 if it fails
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
            fileCreated_date=date.today()
        )

        file_list.append(file_info)
        
    vacancy_application_data = vacancyapplicationfile_schemas.VacancyApplicationCreate(
        vacancy_id=vacancy_id,
        vacancyApplication_category=category,
        vacancyApplication_files=file_list,
        vacancyApplicationCreated_date=date.today()
    )

    new_vacancy_application = vacancyapplicationfile_cruds.create_single_vacancy_application(
        db=db, vacancy_application=vacancy_application_data, category=category
    )

    for file in files:
        vacancyapplicationfile_cruds.upload_file(
            vacancy_id=new_vacancy_application.vacancy_id, 
            vacancy_application_id=new_vacancy_application.vacancyApplication_id, 
            file=file
        )
    
    for file_info in file_list:
        vacancyapplicationfile_cruds.create_vacancy_application_file(
            db=db, vacancyApplication_id=new_vacancy_application.vacancyApplication_id, file=file_info
        )
    
    return new_vacancy_application

@router.get("/{application_id}", response_model=vacancyapplicationfile_schemas.VacancyApplication, 
            status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_user)])
def read_vacancy_application(
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory,
    application_id: Annotated[int, Path(gt=0)], 
    db: Session = Depends(get_db)
    ):

    db_vacancy_application = vacancyapplicationfile_cruds \
        .get_vacancy_application(db, application_id=application_id, category=category)

    if db_vacancy_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Job application with id {application_id} not found"
        )
    
    return db_vacancy_application


@router.get("/", response_model=List[vacancyapplicationfile_schemas.VacancyApplication], 
            status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_user)])
def read_my_vacancy_applications(
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory,
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10, 
    db: Session = Depends(get_db)
    ):

    db_vacancy_applications = vacancyapplicationfile_cruds \
        .get_vacancy_applications(db=db, offset=offset, limit=limit, category=category)

    if db_vacancy_applications is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Application not found"
        )

    return db_vacancy_applications


### I DON'T THINK PATCH IS REQUIRED IN APPLICATIONS
@router.patch("/{application_id}", response_model=vacancyapplicationfile_schemas.VacancyApplication, 
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def update_vacancy_application(
    vacancy_id: Annotated[int, Path(gt=0)],
    vacancy_application_id: Annotated[int, Path(gt=0)],
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory, 
    files: List[UploadFile] = File(...), 
    db: Session = Depends(get_db)
):
    vacancy_application_update = vacancyapplicationfile_schemas.VacancyApplicationUpdate(
        vacancy_id=vacancy_id,
        vacancyApplication_id=vacancy_application_id,
        vacancyApplication_category=category,
        # vacancyApplication_files=[vacancyapplicationfile_schemas.FileCreate(
        #     filename=file.filename,
        #     filedata=decoded_data
        # )],
        vacancyApplicationUpdated_date=date.today()
    )

    updated_vacancy_application = vacancyapplicationfile_cruds.update_vacancy_application(
        db=db, vacancy_id=vacancy_id, vacancy_application_id=vacancy_application_id,
        category=category, vacancy_application_update=vacancy_application_update
    )

    for file in files:
        vacancyapplicationfile_cruds.add_files_to_vacancy_application(
            db=db, vacancy_id=vacancy_id, vacancy_application_id=vacancy_application_id,
            category=category, files=file
        )

    return updated_vacancy_application

### I DON'T THINK DELETE IS REQUIRED IN APPLICATIONS
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_superadmin)])
async def delete_vacancy_application(
    vacancy_id: Annotated[int, Path(gt=0)],
    application_id: Annotated[int, Path(gt=0)],
    category: vacancyapplicationfile_schemas.VacancyApplicationCategory,
    db: Session = Depends(get_db)
):
    vacancy_application = vacancyapplicationfile_cruds.delete_vacancy_application(
        db, vacancy_id, application_id, category
    )

    if not vacancy_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vacancy application with id {application_id} from vacancy with id {vacancy_id} not found."
        )
    
    return vacancy_application

