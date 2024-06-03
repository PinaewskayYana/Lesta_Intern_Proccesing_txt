from fastapi import APIRouter, UploadFile
from services.text_service import TextService
from services.table_service import TableService
from data.database_service import Databaseservice
from .DTO.fileDTO import FileDTO
from config import settings

file_route = APIRouter()
db_serv = Databaseservice(settings.DATABASE_URL_asyncpg)

async def save_uploaded_file(file: UploadFile):
    """
    Сохранение переданного файла
    Возвращает имя файла
    """
    content = file.file.read()
    text_service = TextService(content, db_serv)
    doc_id = await text_service.processing()
    return doc_id

    

@file_route.post("/uploadfile")
async def create_file(file: UploadFile):
    """
    Маршрут для получения и сохранения файла
    Возвращает имя файла 
    """

    docId = await save_uploaded_file(file)
    return FileDTO(doc_id=docId)


@file_route.get("/get_data")
async def create_table(doc_id: str):
    """
    Маршрут для обработки файла
    """
    tb = TableService(db_serv)
    return await tb.choice50(doc_id)
    