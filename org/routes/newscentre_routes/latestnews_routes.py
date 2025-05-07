
from fastapi import APIRouter, status, Depends, Path
from typing import Union, Annotated
from datetime import date
from typing import List

from ...cruds.newscentre_cruds import latestnews_cruds
from ...schemas.newscentre_schemas import latestnews_schemas
from ...utils.auth import get_superadmin
from ...database import db_session

router = APIRouter(
    prefix="/newscentre",
    tags=["News Centre - Latest News"]
)


@router.post("/", response_model=latestnews_schemas.LatestNewsOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_superadmin)])
async def create_latest_news(db: db_session, news_in: latestnews_schemas.LatestNewsIn):
    new_news = latestnews_cruds.create_latest_news(db=db, news_in=news_in)

    return new_news

@router.get("/", response_model=List[latestnews_schemas.LatestNewsOut], status_code=status.HTTP_200_OK)
async def get_all_latest_news(
    db: db_session,
    offset: Union[int, None] = 0,
    limit: Union[Annotated[int, Path(le=10)], None] = 10
):
    all_news = latestnews_cruds.get_all_latest_news(db, offset, limit)

    return all_news

@router.get("/{news_id}", response_model=latestnews_schemas.LatestNewsOut, status_code=status.HTTP_200_OK)
async def get_latest_news(db: db_session, news_id: Annotated[int, Path(gt=0)]):
    news = latestnews_cruds.get_latest_news(db, news_id)

    return news

@router.patch("/{news_id}", response_model=latestnews_schemas.LatestNewsOut, status_code=status.HTTP_201_CREATED,
              dependencies=[Depends(get_superadmin)])
async def update_latest_news(
    heading: str, info: str,
    db: db_session, news_id= Annotated[int, Path(gt=0)]
):
    news_data = latestnews_schemas.LatestNewsUpdate(
        news_id=news_id,
        news_heading=heading,
        news_info=info,
        newsUpdated_date=date.today()
    )

    update_news = latestnews_cruds.update_latest_news(db=db, news_id=news_id, news_update=news_data)

    return update_news

@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_superadmin)])
async def delete_latest_news(db: db_session, news_id: Annotated[int, Path(gt=0, description="Insert news ID")]):
    delete_news = latestnews_cruds.delete_latest_news(db=db, news_id=news_id)

    return delete_news
