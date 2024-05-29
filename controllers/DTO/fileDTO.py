from pydantic import BaseModel

class FileDTO(BaseModel):
    doc_id: str