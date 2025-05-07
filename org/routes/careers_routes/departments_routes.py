
from fastapi import APIRouter, UploadFile, File, Depends, status, Path
from typing import List, Union, Annotated

from ...schemas.careers_schemas import departments_schemas
from ...cruds.careers_cruds import departments_cruds
from ...database import db_session
from ...utils.auth import get_superadmin

router = APIRouter(
    prefix="/departments",
    tags=["Careers - Departments"]
)

@router.post("/", response_model=departments_schemas.Department,
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def create_department(
    db: db_session,
    title: str,
    department_image: UploadFile = File(...)
):
    department = departments_cruds.create_department(db, title, department_image)

    return department


@router.get("/{department_id}", response_model=departments_schemas.Department,
            status_code=status.HTTP_200_OK)
async def get_department(db: db_session, department_id: Annotated[int, Path(gt=0)]):
    department = departments_cruds.get_department(db, department_id)

    return department


@router.get("/", response_model=List[departments_schemas.Department],
            status_code=status.HTTP_200_OK)
async def get_departments(
    db: db_session, 
    offset: Union[int, None] = 0,
    limit: Union[Annotated[int, Path(le=10)], None] = 10
):
    departments = departments_cruds.get_departments(db, offset, limit)

    return departments


@router.patch("/{department_id}", response_model=departments_schemas.Department,
              status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def update_department(
    db: db_session,
    department_id: Annotated[int, Path(gt=0)],
    title: str,
    department_image: UploadFile = File(...)
):
    department = departments_cruds.update_department(db, department_id, title, department_image)

    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_superadmin)])
async def delete_department(
    db: db_session,
    department_id: Annotated[int, Path(gt=0)]
):
    department = departments_cruds.delete_department(db, department_id)

    return department