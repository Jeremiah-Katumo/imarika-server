from pydantic import BaseModel

class ImageBase(BaseModel):
    title: str

class ImageCreate(ImageBase):
    # id: int
    # filename: str

    class Config:
        from_attributes = True

class ImageUpdate(ImageBase):
    id: int
    filename: str

    class Config:
        from_attributes = True

class ImageOut(ImageBase):
    id: int
    filename: str

    class Config:
        from_attributes = True