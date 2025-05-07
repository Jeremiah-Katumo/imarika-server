
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...models import org_models
from ...schemas.newscentre_schemas import latestnews_schemas


def create_latest_news(db: Session, news_in: latestnews_schemas.LatestNewsIn) -> org_models.LatestNews:
    news_exist = db.query(org_models.LatestNews) \
        .filter(org_models.LatestNews.news_heading == news_in.news_heading) \
            .first()
    if news_exist != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"News {news_in.news_heading} already exists"
        )
    
    new_news = org_models.LatestNews(
        news_heading=news_in.news_heading,
        news_info=news_in.news_info,
        newsCreated_date=news_in.newsCreated_date,
        newsUpdated_date=news_in.newsUpdated_date,
        newsCreated_by=news_in.newsCreated_by,
        newsUpdated_by=news_in.newsUpdated_by
    )

    db.add(new_news)
    db.commit()
    db.refresh(new_news)

    return new_news


def get_all_latest_news(db: Session, offset: int, limit: int) -> List[latestnews_schemas.LatestNewsOut]:
    all_news = db.query(org_models.LatestNews) \
        .offset(offset).limit(limit).all()
    
    if all_news is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No news found"
        )
    
    return [latestnews_schemas.LatestNewsOut.from_orm(news) for news in all_news]


def get_latest_news(db: Session, news_id: int):
    news = db.query(org_models.LatestNews) \
        .filter(org_models.LatestNews.news_id == news_id) \
            .first()
    
    if news == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News with id {news_id} not found"
        )
    
    return news


def update_latest_news(
        db: Session, news_id: int, 
        news_update: latestnews_schemas.LatestNewsUpdate
    ) -> org_models.LatestNews:
    news_exist = db.query(org_models.LatestNews) \
        .filter(org_models.LatestNews.news_id == news_id) \
            .first()
    
    if news_exist == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News with id {news_id} not found"
        )
    
    if news_update.news_heading is not None:
        news_exist.news_heading=news_update.news_heading
    if news_update.news_info is not None:
        news_exist.news_info=news_update.news_info

    db.commit()
    db.refresh(news_exist)

    return news_exist


def delete_latest_news(db: Session, news_id: int):
    delete_news = db.query(org_models.LatestNews) \
        .filter(org_models.LatestNews.news_id == news_id) \
            .first()
    
    if delete_news == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News with id {news_id} not found"
        )
    
    db.delete(delete_news)
    db.commit()

    return delete_news
