from pydantic import BaseModel

class FileDTO(BaseModel):
    filename: str