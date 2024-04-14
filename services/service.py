from fastapi import FastAPI, APIRouter

from controllers.file_controller import file_route
from data.database_service import Databaseservice
from pages.router import router_page

class APIService:
    """
    Класс APIService используется для инициализации API-сервиса, 
    используя FastAPI

    Атрибуты:
    ----------
    database: Databaseservice
        Сервис базы данных
    debug: bool
        Флаг отладки
    app: FastAPI
        Экземпляр FastAPI
    
    Метод:
    ----------
    add_routers:
        Подключение маршрутов к API
    """

    def __init__(self, database: Databaseservice):
        self.debug= True
        self.app = FastAPI(
            title="TfIdf"
        )

        self.database = database
        self.app.state.database = database

        self.add_routers()
    
    def add_routers(self):
        api_router = APIRouter(prefix="/api")

        self.app.include_router(router=api_router)
        self.app.include_router(router=file_route, prefix="/api/file")
        self.app.include_router(router=router_page)
