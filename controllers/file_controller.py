from fastapi import APIRouter, UploadFile
from services.text_service import TextService
from data.database_service import Databaseservice
from .DTO.fileDTO import FileDTO
from config import settings
import os

file_route = APIRouter()
db_serv = Databaseservice(settings.DATABASE_URL_asyncpg)

async def save_uploaded_file(file: UploadFile):
    """
    Сохранение переданного файла
    Возвращает имя файла
    """

    directory = os.getcwd()
    directory += '/controllers/uploaded_files'
    path = os.path.join(directory, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return file.filename


async def prosecc_file(filename: str):
    """
    Принимает имя файла, читает его содержимое
    Обрабатывает файл
    """

    directory = os.getcwd()
    directory += '/controllers/uploaded_files'
    path = os.path.join(directory, filename)
    with open(path, mode='rb') as f:
        content = f.read()
    text_service = TextService(content, db_serv)
    return await text_service.processing()
    

@file_route.post("/uploadfile")
async def create_file(file: UploadFile):
    """
    Маршрут для получения и сохранения файла
    Возвращает имя файла 
    """

    filename = await save_uploaded_file(file)
    return {"filename": filename}


@file_route.get("/get_name")
async def process_file(f: FileDTO):
    """
    Получение имени файла, передаваемого в запросе
    """

    name = f.filename
    return name


@file_route.get("/get_data")
async def create_table(name: str):
    """
    Маршрут для обработки файла
    """
    
    return await prosecc_file(name)
    