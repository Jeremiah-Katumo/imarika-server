
from pydantic import BaseModel
from datetime import datetime, date


class LatestNewsBase(BaseModel):
    # news_heading: str
    # news_info: str
    newsCreated_date: datetime
    newsUpdated_date: date | None = None
    newsCreated_by: int | None = None
    newsUpdated_by: int | None = None

class LatestNewsIn(LatestNewsBase):
    news_heading: str
    news_info: str

class LatestNewsOut(LatestNewsBase):
    news_id: int
    news_heading: str
    news_info: str

    class Config:
        from_attributes = True
        from_attributes = True

class LatestNewsUpdate(BaseModel):
    news_id: int
    news_heading: str
    news_info: str
    newsUpdated_date: date | None = None
    newsCreated_by: int | None = None
    newsUpdated_by: int | None = None