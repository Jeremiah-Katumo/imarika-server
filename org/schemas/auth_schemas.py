from pydantic import BaseModel, EmailStr

# class User(BaseModel):
#     email: EmailStr
#     username: str
#     full_name: str
#     disabled: bool
#     is_superuser: bool

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str | None = None
    # id: int | None = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = True
    is_superuser: bool = False

    # class Config:
    #     orm_mode = True


class UserInDB(UserBase):
    hashed_password: str

    # class Config:
    #     orm_mode = True

class User(UserBase):
    id: int 

    class Config:
        orm_mode = True