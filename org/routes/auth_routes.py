
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..schemas import auth_schemas
from ..cruds import auth_cruds
from ..utils import auth
from ..database import get_db, db_session


load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=auth_schemas.User)
async def signup(user: auth_schemas.UserInDB, db: Session = Depends(get_db)):
    db_user = auth_cruds.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    new_user = auth_cruds.create_user(db=db, user=user)

    return new_user

# @router.post("/token", response_model=dict)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = auth_cruds.get_user_by_email(db, email=form_data.username)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     if not auth.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     access_token = auth.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}
@router.post("/token", response_model=auth_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or password are required"
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    # create an access_token using username and expiration time
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", status_code=status.HTTP_200_OK, response_model=auth_schemas.User)
async def read_users_me(current_user: auth_schemas.User = Depends(auth.get_current_active_user)):
    
    return current_user
