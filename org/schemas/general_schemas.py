from fastapi import UploadFile
from datetime import datetime, date
from typing import Union, List
from enum import Enum
from uuid import UUID

class ImageTypeFileExtensions(str, Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"

class DocTypeFileExtensions(str, Enum):
    pdf = "pdf"
    csv = "csv"
    doc = "doc"
    docx = "docx"