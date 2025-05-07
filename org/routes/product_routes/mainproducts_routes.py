
from fastapi import APIRouter, status, Depends, UploadFile, File, Path
from sqlalchemy.orm import Session
from typing import Annotated

from ...schemas.product_schemas import mainproducts_schemas
from ...cruds.product_cruds import mainproducts_cruds
from ...database import get_db
from ...utils.auth import get_superadmin


router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.post("/", response_model=mainproducts_schemas.Product, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_superadmin)])
async def create_product(
    title: str, description: str,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    db: Session = Depends(get_db),
    product_image: UploadFile = File(...)
    ):

    new_product = mainproducts_cruds.create_product(
        db=db, 
        title=title, 
        description=description, 
        category=category, 
        sub_category=sub_category,
        product_image=product_image
    )

    return new_product


@router.get("/", response_model=mainproducts_schemas.Product, status_code=status.HTTP_200_OK)
async def get_category_products(
    category: mainproducts_schemas.ProductCategory, 
    db: Session = Depends(get_db)
    ):

    category_products = mainproducts_cruds.get_category_products(
        db=db, 
        category=category
    )

    return category_products


@router.get("/{product_id}", response_model=mainproducts_schemas.Product, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: Annotated[int, Path(gt=0)],
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    db: Session = Depends(get_db)
):
    product = mainproducts_cruds.get_product_by_id(db=db, product_id=product_id, category=category, sub_category=sub_category)

    return product


@router.patch("/{product_id}", response_model=mainproducts_schemas.Product, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(get_superadmin)])
async def update_product(
    product_id: int, title: str, description: str,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    db: Session = Depends(get_db)
):
    updated_product = mainproducts_cruds.update_product(
        db=db, 
        product_id=product_id, 
        title=title, 
        description=description, 
        category=category, 
        sub_category=sub_category
    )

    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_superadmin)])
async def delete_product(
    product_id: Annotated[int, Path(gt=0)],
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    db: Session = Depends(get_db)
):
    deleted_product = mainproducts_cruds.delete_product(
        db=db, 
        product_id=product_id, 
        category=category, 
        sub_category=sub_category
    )

    return deleted_product
