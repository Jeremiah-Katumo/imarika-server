
from fastapi import APIRouter, UploadFile, File, Depends, status, Path
from typing import List, Union, Annotated
from sqlalchemy.orm import Session

from ...schemas.careers_schemas import team_schemas
from ...cruds.careers_cruds import team_cruds
from ...database import get_db
from ...utils.auth import get_superadmin

router = APIRouter(
    prefix="/team",
    tags=['Careers - Team']
)

@router.post("/org_members", response_model=team_schemas.TeamMember, 
             status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def create_team_member(
    name: str, 
    org_id: Annotated[int, Path(gt=0)],
    email: str,
    phone: Union[str, None] = None,
    profile_picture: UploadFile = File(...), 
    position: Union[team_schemas.Positions, None] = None, 
    social_media_links: Union[List[str], None] = [],
    db: Session = Depends(get_db)
):
    member = team_cruds.create_member(
        db=db,
        name=name,
        org_id=org_id,
        email=email,
        phone=phone,
        profile_picture=profile_picture,
        position=position,
        social_media_links=social_media_links
    )

    return member

@router.get("/org_members", status_code=status.HTTP_200_OK, 
            response_model=List[team_schemas.TeamMember])
async def read_all_members(
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10, 
    db: Session = Depends(get_db)
):
    members = team_cruds.get_all_members(db, offset, limit)

    return members

@router.get("/org_members/{org_id}", status_code=status.HTTP_200_OK,
             response_model=List[team_schemas.TeamMember])
async def read_org_members(
    org_id: Annotated[int, Path(gt=0)], 
    offset: Union[int, None] = 0, 
    limit: Union[Annotated[int, Path(le=10)], None] = 10, 
    db: Session = Depends(get_db)
):
    org_members = team_cruds.get_org_members(db, org_id, offset, limit)

    return org_members

@router.get("/org_members/{org_id}/member/{member_id}", status_code=status.HTTP_200_OK,
            response_model=team_schemas.TeamMember)
async def read_single_team_member(
    org_id: Annotated[int, Path(gt=0)], 
    member_id: Annotated[int, Path(gt=0)], 
    db: Session = Depends(get_db)
):
    single_team_member = team_cruds.get_single_team_member(db, org_id, member_id)

    return single_team_member

@router.patch("/org_members/{org_id}/member/{member_id}", response_model=team_schemas.TeamMember, 
              status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_superadmin)])
async def update_team_member(
    member_id: Annotated[int, Path(gt=0)],
    org_id: Annotated[int, Path(gt=0)],
    name: Union[str, None] = None,
    profile_picture: Union[UploadFile, None] = File(None),
    position: Union[team_schemas.Positions, None] = None,
    social_media_links: Union[List[str], None] = None,
    phone: Union[str, None] = None,
    email: Union[str, None] = None,
    db: Session = Depends(get_db)
):
    updated_member = team_cruds.update_member(
        db=db,
        member_id=member_id,
        org_id=org_id,
        name=name,
        profile_picture=profile_picture,
        position=position,
        social_media_links=social_media_links,
        phone=phone,
        email=email
    )

    return updated_member

@router.delete("/org_members/{org_id}/member/{member_id}", status_code=status.HTTP_204_NO_CONTENT, 
               dependencies=[Depends(get_superadmin)])
async def delete_team_member(
    org_id: Annotated[int, Path(gt=0)], 
    member_id: Annotated[int, Path(gt=0)], 
    db: Session = Depends(get_db)
):
    deleted_item = team_cruds.delete_member(db, org_id, member_id)

    return deleted_item
