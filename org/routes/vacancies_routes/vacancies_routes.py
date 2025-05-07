
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List, Union, Annotated

from ...database import get_db
from ...schemas.vacancies_schemas import vacancies_schemas
from ...cruds.vacancies_cruds import vacancies_cruds
from ...utils.auth import get_superadmin

router = APIRouter(
    prefix="/vacancies",
    tags=['Vacancies']
)

# JOBS ROUTES
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[vacancies_schemas.Vacancy])
async def read_vacancies(
    category: vacancies_schemas.VacancyCategory,
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10,
    db: Session = Depends(get_db)
    ):

    vacancies = vacancies_cruds.get_vacancies(db=db, category=category, offset=offset, limit=limit)

    return vacancies

@router.post("/", response_model=vacancies_schemas.Vacancy, status_code=status.HTTP_201_CREATED, 
             dependencies=[Depends(get_superadmin)])
async def create_vacancy(category: vacancies_schemas.VacancyCategory, vacancy: vacancies_schemas.VacancyCreate, db: Session = Depends(get_db)):
    new_vacancy = vacancies_cruds.create_vacancy(db=db, vacancy=vacancy, category=category)

    return new_vacancy

@router.patch("/{vacancy_id}", response_model=vacancies_schemas.Vacancy, 
              status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def update_job(
    category: vacancies_schemas.VacancyCategory,
    vacancy_id: Annotated[int, Path(gt=0)], 
    vacancy: vacancies_schemas.VacancyCreate, 
    db: Session = Depends(get_db)
    ):

    db_vacancy = vacancies_cruds.get_vacancy(db=db, vacancy_id=vacancy_id, category=category)

    if not db_vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Job not found"
        )
    
    update_vacancy = vacancies_cruds.update_vacancy(db=db, vacancy_id=vacancy_id, vacancy=vacancy, category=category)
    
    return update_vacancy

@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
async def delete_job(
    category: vacancies_schemas.VacancyCategory,
    vacancy_id: Annotated[int, Path(gt=0)], 
    db: Session = Depends(get_db)
    ):

    db_vacancy = vacancies_cruds.get_vacancy(db, vacancy_id=vacancy_id, category=category)

    if not db_vacancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Job not found"
        )
    
    delete_vacancy = vacancies_cruds.delete_job(db=db, vacancy_id=vacancy_id, category=category)

    return delete_vacancy
