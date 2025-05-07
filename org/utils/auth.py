
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import org_models
from ..schemas.auth_schemas import UserBase
from ..schemas import auth_schemas


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#### USER 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


#### GET USER
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return auth_schemas.UserInDB(**user_dict)
def get_user(db, username: str):
    user = db.query(org_models.User) \
        .filter(org_models.User.username == username) \
            .first()

    return user
# def get_user(current_user: dict = Depends(get_current_user)):
#     if current_user["role"] not in ["superadmin", "superuser", "user"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Operation not permitted",
#         )
#     return current_user


#### AUTHENTICATE USER
def authenticate_user(db, username: str, password: str):
    # user = get_user(fake_db, username)
    user = db.query(org_models.User) \
        .filter(org_models.User.username == username) \
            .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


#### CREATE ACCESS TOKEN
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


#### GET CURRENT USER
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # user_id: int = payload.get("user_id")
        if username is None:
            raise credentials_exception
        
        token_data = auth_schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(db, username=token_data.username)

    if user is None:
        raise credentials_exception
    
    return user
# async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, email=email)
#     if user is None:
#         raise credentials_exception
#     return user
#####
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     # Here you should implement your own token validation logic
#     if token == "superadmin":
#         return {"role": "superadmin"}
#     elif token == "superuser":
#         return {"role": "superuser"}
#     elif token == "user":
#         return {"role": "user"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


#### GET CURRENT ACTIVE USER
async def get_current_active_user(current_user: auth_schemas.UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return current_user


#### GET SUPERADMIN
async def get_superadmin(current_user: Annotated[UserBase, Depends(get_current_user)]):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have the required permissions"
        )
    
    return current_user
# async def get_superadmin(current_user: dict = Depends(get_current_user)):
#     if current_user["role"] != "superadmin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Operation not permitted",
#         )
#     return current_user
# def get_superuser_or_superadmin(current_user: dict = Depends(get_current_user)):
#     if current_user["role"] not in ["superadmin", "superuser"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Operation not permitted",
#         )
#     return current_user


#### CREATE SUPERADMIN
async def create_superadmin(db: Session, user: auth_schemas.UserInDB):
    db_user = org_models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.hashed_password),
        is_superadmin=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
