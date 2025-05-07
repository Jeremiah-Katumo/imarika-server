
from fastapi import status, HTTPException, UploadFile, File, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Union, Annotated
import os 
import uuid
from datetime import date

from ...schemas.careers_schemas import team_schemas
from ...schemas import general_schemas
from ...models import org_models
from ...utils.utils import check_image_type_file_extension


def create_single_member(
        db: Session, 
        name: str, 
        org_id: Annotated[int, Path(gt=0)],
        email: str,
        profile_picture: UploadFile = File(...), 
        position: Union[team_schemas.Positions, None] = None, 
        social_media_links: Union[List[str], None] = [],
        phone: Union[str, None] = None
    ) -> team_schemas.TeamMember:
   
    member_in_db = db.query(org_models.TeamMember) \
        .filter(org_models.TeamMember.email == email) \
            .first()

    if member_in_db !=  None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail=f'Member with email {email} already exists'
        )

    db_member = org_models.TeamMember(
        name = name, 
        org_id = org_id,
        profile_picture = profile_picture, 
        position = position, 
        social_media_links = social_media_links,
        phone = phone,
        email = email,
        created_date = date.today()
    )
    
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member

def get_file_extension(profile_picture: UploadFile) -> general_schemas.ImageTypeFileExtensions:
    # extract filename from the profile_picture
    filename = profile_picture.filename
    # split filename using the dot (.) as the delimiter. 
    # The last element of the split result (which is at index -1) represents the file extension.
    file_extension = filename.split('.')[-1].lower()

    return file_extension

def hashed_filename_profile_picture(profile_picture: UploadFile) -> UploadFile:
    file_hash = uuid.uuid4()
    
    profile_picture.filename = f"{file_hash}.{get_file_extension(profile_picture)}"

    return profile_picture

def upload_file(org_id: int, member_id: int, profile_picture: UploadFile) -> str:
    # check the file size of the profile picture exceeds 2 MB
    if profile_picture.size > 2 * 1024 * 1024:  # 2 MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only files of size 2 MB or below are allowed"
        )
    # construct the directory path where the profile picture be stored based on the organization id and member id
    org = f"org_{str(org_id)}"
    member = f"member_{str(member_id)}"
    profile_picture_image_path = os.path.join("storage","organisation","images","profile_pictures",org,member)
    # if directory path does not exist create it 
    if not os.path.exists(profile_picture_image_path):
        os.makedirs(profile_picture_image_path)
    # construct the full file path by joining the directory path and the filename of the profile picture
    full_file_path = os.path.join(profile_picture_image_path, profile_picture.filename)
    # Checks if a file with the same name already exists in the directory. If it does, it removes the existing file.
    if os.path.exists(full_file_path):
        os.remove(full_file_path)
    # Opens the full file path in write binary mode and writes the contents of the profile picture file to it.
    with open(full_file_path, "wb") as image:
        image.write(profile_picture.file.read())

    return profile_picture.filename

def create_member(
        db: Session, 
        name: str, 
        org_id: Annotated[int, Path(gt=0)],
        email: str,
        phone: Union[str, None] = None,
        profile_picture: UploadFile = File(...),
        position: Union[team_schemas.Positions, None] = None, 
        social_media_links: Union[List[str], None] = []
    ) -> team_schemas.TeamMemberBase:
    # check if a profile picture was provided and if it's a valid image file (PNG or JPEG) specified in utils
    if profile_picture and not check_image_type_file_extension(get_file_extension(profile_picture)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only png, jpeg and jpg file formats are allowed"
        )

    new_file = None
    if profile_picture:
        update_profile_picture = hashed_filename_profile_picture(profile_picture)
        new_file = update_profile_picture.filename 
    # create a new team member record in the database
    new_member = create_single_member(
        db = db, 
        name = name, 
        org_id = org_id,
        profile_picture = new_file, 
        position = position, 
        social_media_links = social_media_links,
        phone =  phone,
        email = email
    )
    # updload profile picture
    if profile_picture:
        upload_file(org_id, new_member.id, hashed_filename_profile_picture(profile_picture))

    return new_member

def get_all_members(
        db: Session, 
        offset: Union[int, None] = 0, 
        limit: Union[Annotated[int, Path(le=10)], None] = 10
    ):
    members = db.query(org_models.TeamMember) \
        .order_by(desc(org_models.TeamMember.created_date)) \
            .limit(limit).offset(offset).all()
        
    if members is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No members found"
        )
    
    return members

def get_org_members(db: Session, org_id: Annotated[int, Path(gt=0)], offset: int, limit: int):
    members = db.query(org_models.TeamMember) \
        .filter(org_models.TeamMember.org_id == org_id) \
            .order_by(desc(org_models.TeamMember.created_date)) \
                .limit(limit).offset(offset).all()
        
    if len(members) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No members found for org Id {org_id}"
        )

    return members

def get_single_team_member(db: Session, org_id: Annotated[int, Path(gt=0)], member_id: Annotated[int, Path(gt=0)]):
    member = db.query(org_models.TeamMember) \
        .filter(org_models.TeamMember.id == member_id) \
            .filter(org_models.TeamMember.org_id == org_id) \
                .first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Member of id {member_id} and Org Id {org_id} not found'
        )
    
    return member

def update_member(
    db: Session,
    member_id: Annotated[int, Path(gt=0)],
    org_id: Annotated[int, Path(gt=0)],
    name: Union[str, None] = None,
    profile_picture: UploadFile = File(...),
    position: Union[team_schemas.Positions, None] = None,
    social_media_links: Union[List[str], None] = [],
    phone: Union[str, None] = None,
    email: Union[str, None] = None
):
    member = db.query(org_models.TeamMember) \
        .filter(org_models.TeamMember.id == member_id) \
            .filter(org_models.TeamMember.org_id == org_id) \
                .first()
    # check if member not found in db
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Member with id {member_id} not found'
        )
    # verifies that the file size is within the allowed limit (2 MB or below)
    if profile_picture:
        if profile_picture.size > 2000000:  # 2 MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Only files of size 2 MB or below are allowed"
            )
        # Check if the profile picture file is a valid image file (PNG, JPEG). Deny uploads of types not png and jpeg/jpg
        if not check_image_type_file_extension(get_file_extension(profile_picture)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Only png and jpg file formats are allowed"
            )
        # Update the UploadFile to have a hashed filename
        profile_picture = hashed_filename_profile_picture(profile_picture)
        profile_picture_filename = profile_picture.filename
        # Upload the profile photo
        upload_file(member.org_id, member_id, profile_picture)

        member.profile_picture = profile_picture_filename
    # update member information in the database based on provided parameters
    if name is not None:
        member.name = name
    if position is not None:
        member.position = position
    if social_media_links is not None:
        member.social_media_links = social_media_links
    if phone is not None:
        member.phone = phone
    if email is not None:
        member.email = email

    db.commit()
    db.refresh(member)

    return member

def delete_member(db: Session, org_id: Annotated[int, Path(gt=0)], member_id: Annotated[int, Path(gt=0)]):
    member = db.query(org_models.TeamMember) \
        .filter(org_models.TeamMember.id == member_id) \
            .filter(org_models.TeamMember.org_id == org_id) \
                .first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Member of id {member_id} and Org Id {org_id} not found'
        )

    db.delete(member)
    db.commit()

    return member
