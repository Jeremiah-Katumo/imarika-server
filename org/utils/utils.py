
import json
from sqlalchemy import TypeDecorator, Text

from ..schemas.general_schemas import ImageTypeFileExtensions, DocTypeFileExtensions


class ListType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


def check_image_type_file_extension(extension):
    try:
        ImageTypeFileExtensions(extension)
        return True
    except ValueError:
        return False

def check_doc_type_file_extension(extension):
    try:
        DocTypeFileExtensions(extension)
        return True
    except ValueError:
        return False
    
