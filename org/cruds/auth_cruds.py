
from sqlalchemy.orm import Session

from ..models import org_models
from ..schemas import auth_schemas
from ..utils import auth 

def get_user(db: Session, user_id: int):
    user = db.query(org_models.User) \
        .filter(org_models.User.id == user_id) \
            .first()
    
    return user

def get_user_by_email(db: Session, email: str):
    user_by_email = db.query(org_models.User) \
        .filter(org_models.User.username == email) \
            .first()
    
    return user_by_email

def create_user(db: Session, user: auth_schemas.UserInDB):
    hashed_password = auth.get_password_hash(user.hashed_password)

    db_user = org_models.User(
        email=user.email, 
        hashed_password=hashed_password,   # the hashed_password at the right sight of the = sign is from auth.get_password_hash
        username=user.username,
        full_name=user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(org_models.User) \
        .offset(skip).limit(limit).all()
    
    return users
