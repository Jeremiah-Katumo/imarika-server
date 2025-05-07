
import os
import uuid
from fastapi import Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from ...models import org_models
from ...schemas import general_schemas
from ...schemas.product_schemas import mainproducts_schemas
from ...utils.utils import check_image_type_file_extension


def create_single_product(
    db: Session, title: str, description: str,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    product_image: UploadFile = File(...)
    ) -> mainproducts_schemas.ProductBase:

    product_in_db = db.query(org_models.Product) \
        .filter(org_models.Product.product_title == title) \
            .filter(org_models.Product.product_category == category) \
                .filter(org_models.Product.productSub_category == sub_category) \
                    .first()
    
    if product_in_db != None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Product '{title}' already exists"
        )
    
    db_product = org_models.Product(
        product_title = title,
        product_description = description,
        product_category = category,
        productSub_category = sub_category,
        product_image = product_image
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_image_extension(product_image: UploadFile) -> general_schemas.ImageTypeFileExtensions:
    # extract filename from the profile_picture
    filename = product_image.filename
    # split filename using the dot (.) as the delimiter. 
    # The last element of the split result (which is at index -1) represents the file extension.
    file_extension = filename.split('.')[-1].lower()

    return file_extension

def hashed_product_image(product_image: UploadFile) -> UploadFile:
    image_hash = uuid.uuid4()
    
    product_image.filename = f"{image_hash}.{get_image_extension(product_image)}"

    return product_image
    

def upload_file(product_id: int, product_image: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if product_image.size > 2 * 1024 * 1024:  # 2 MB
        raise HTTPException(
            status_code=400, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    product = f"product_{str(product_id)}"
    product_image_path = os.path.join("storage","Products","images","product_images",product)
    # if directory path does not exist create it 
    if not os.path.exists(product_image_path):
        os.makedirs(product_image_path)
    # construct the full file path by joining the directory path and the filename of the profile picture
    full_image_path = os.path.join(product_image_path, product_image.filename)
    # Checks if a file with the same name already exists in the directory. If it does, it removes the existing file.
    if os.path.exists(full_image_path):
        os.remove(full_image_path)
    # Opens the full file path in write binary mode and writes the contents of the profile picture file to it.
    with open(full_image_path, "wb") as image:
        image.write(product_image.file.read())

    return product_image.filename


def create_product(
    db: Session, title: str, description: str,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    product_image: UploadFile = File(...)
    ):

    if product_image and not check_image_type_file_extension(get_image_extension(product_image)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only png and jpg file formats are allowed"
        )

    new_file = None
    if new_file:
        update_image = hashed_product_image(product_image)
        new_file = update_image.filename

    new_image = create_single_product(
        db=db,
        title=title,
        description=description,
        category=category,
        sub_category=sub_category,
        product_image=new_file
    )

    if product_image:
        upload_file(new_image.product_id, hashed_product_image(product_image))

    return new_image


def get_products(
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    db: Session, offset: int = 0, limit: int = 10
    ):

    products = db.query(org_models.Product) \
        .filter(org_models.Product.product_category == category) \
            .filter(org_models.Product.productSub_category == sub_category) \
                .offset(offset).limit(limit).all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No products found for category '{category}' and sub category '{sub_category}'"
        )
    
    return products


def get_product_by_id(
    db: Session, product_id: int, category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory
    ):

    product = db.query(org_models.Product) \
        .filter(org_models.Product.product_id == product_id) \
            .filter(org_models.Product.product_category == category) \
                .filter(org_models.Product.productSub_category == sub_category) \
                    .first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No product found for id '{product_id}'"
        )
    
    return product


def get_category_products(
    db: Session, category: mainproducts_schemas.ProductCategory
):
    products = db.query(org_models.Product) \
        .filter(org_models.Product.product_category == category) \
            .all()
    
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No products found for category '{category}'"
        )
    
    return products


def update_product(
    db: Session, product_id: int, title: str, description: str,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory,
    product_image: UploadFile = File(...)
):
    product = db.query(org_models.Product) \
        .filter(org_models.Product.product_id == product_id) \
            .filter(org_models.Product.product_category == category) \
                .filter(org_models.Product.productSub_category == sub_category) \
                    .first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No product found for id '{product_id}'"
        )
    
    if product_image:
        if product_image.size > 2000000: # 2 MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Only files of size 2 MB or below are allowed"
            )

        if not check_image_type_file_extension(get_image_extension(product_image)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Only png and jpg file formats are allowed"
            )
        
        product_image = hashed_product_image(product_image)
        product_image_name = product_image.filename

        upload_file(product_id, product_image)

        product.product_image = product_image_name

    if title is not None:
        product.product_title = title
    if description is not None:
        product.product_description = description
    if category is not None:
        product.product_category = category
    if sub_category is not None:
        product.productSub_category = sub_category

    db.commit()
    db.refresh(product)

    return product



def delete_product(
    db: Session, product_id: int,
    category: mainproducts_schemas.ProductCategory,
    sub_category: mainproducts_schemas.ProductSubCategory
):
    product = db.query(org_models.Product) \
        .filter(org_models.Product.product_id == product_id) \
            .filter(org_models.Product.product_category == category) \
                .filter(org_models.Product.productSub_category == sub_category) \
                    .first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No product found for id '{product_id}'"
        )
    
    db.delete(product)
    db.commit()

    return product