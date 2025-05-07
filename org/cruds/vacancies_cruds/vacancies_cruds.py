
from fastapi import Path
from sqlalchemy.orm import Session
from typing import Annotated, Union

from ...models import org_models
from ...schemas.vacancies_schemas import vacancies_schemas


# JOBS CRUDS
def get_vacancy(db: Session, vacancy_id: Annotated[int, Path(gt=0)], category: vacancies_schemas.VacancyCategory):
    vacancy = db.query(org_models.Vacancy) \
        .filter(org_models.Vacancy.vacancy_id == vacancy_id) \
            .filter(org_models.Vacancy.category == category) \
                .first()
    
    return vacancy

def get_vacancies(
        category: vacancies_schemas.VacancyCategory, 
        db: Session, 
        offset: Union[int, None] = 0, 
        limit: Union[Annotated[int, Path(le=10)], None] = 10
    ):
    vacancies = db.query(org_models.Vacancy) \
        .filter(org_models.Vacancy.category == category) \
            .limit(limit).offset(offset).all()
    
    return vacancies

def create_vacancy(db: Session, vacancy: vacancies_schemas.VacancyCreate, category: vacancies_schemas.VacancyCategory):
    db_vacancy = org_models.Vacancy(**vacancy.dict())

    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)

    return db_vacancy

def update_vacancy(db: Session, vacancy_id: Annotated[int, Path(gt=0)], category: vacancies_schemas.VacancyCategory, vacancy: vacancies_schemas.VacancyCreate):
    db_vacancy = db.query(org_models.Vacancy) \
        .filter(org_models.Vacancy.vacancy_id == vacancy_id) \
            .filter(org_models.Vacancy.category == category) \
                .first()
    
    if db_vacancy:
        for key, value in vacancy.dict().items():
            setattr(db_vacancy, key, value)
        db.commit()
        db.refresh(db_vacancy)

    return db_vacancy

def delete_job(db: Session, vacancy_id: Annotated[int, Path(gt=0)], category: vacancies_schemas.VacancyCategory):
    db_vacancy = db.query(org_models.Vacancy) \
        .filter(org_models.Vacancy.vacancy_id == vacancy_id) \
            .filter(org_models.Vacancy.category == category) \
                .first()
    
    if db_vacancy:
        db.delete(db_vacancy)
        db.commit()

    return db_vacancy

