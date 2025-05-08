from pydantic import BaseModel
from enum import Enum
from typing import Union


class ProductCategory(str, Enum):
    membership = "Membership"
    savings_products = "Savings products"
    agribusiness_financing = "Agribusiness products"
    education_financing = "Education financing"
    e_channels = "E - Channels"

class ProductSubCategory(str, Enum):
    membership_individuals = "Membership Individuals"
    membership_institutions = "Membership Institutions"
    membership_groups = "Membership Groups"
    savings_ordinary = "Savings Ordinary"
    savings_malaika = "Savings Malaika"
    savings_holiday = "Savings Holiday"
    savings_fixed = "Savings Fixed"
    savings_ekeza = "Savings Ekeza"
    savings_jipange = "Savings Jipange"
    agribusiness_kilimo = "Agribusiness Kilimo"
    agribusiness_ufugaji = "Agribusiness Ufugaji"
    agribusiness_mtaji = "Agribusiness Mtaji"
    agribusiness_maziwa = "Agribusiness Maziwa"
    education_schoolfees = "Education School Fees"
    education_scholarplus = "Education Scholarplus"
    echannels_m_banking = "E-channels M-banking"
    echannels_paybill = "E-channels Paybill"
    echannels_sacco = "E-channels Sacco Agency"
    echannels_atm = "E-channels ATM"


class ProductBase(BaseModel):
    product_id: int
    product_title: str


class ProductCreate(ProductBase):
    product_description: str
    product_image: Union[str, None] = None
    product_category: str
    productSub_category: str

    class Config:
        # from_attributes = True
        from_attributes = True


class Product(ProductBase):
    product_id: int
    product_description: str
    product_image: Union[str, None] = None
    product_category: str
    productSub_category: str

    class Config:
        # from_attributes = True
        from_attributes = True
