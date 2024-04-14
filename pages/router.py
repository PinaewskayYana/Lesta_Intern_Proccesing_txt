from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from controllers.file_controller import create_table

router_page = APIRouter()

templates = Jinja2Templates(directory="templates")

@router_page.get("/")
async def get_uploud_page(request: Request):
    """
    Обработка маршрута для страницы загрузки файла

    Параметр:
    ----------------
    request: Request
        Объект запроса FastAPI

    Возвращает шаблон страницы загрузки файла   
    """

    return templates.TemplateResponse("uploud_file.html", {"request": request})


@router_page.get("/page/table/{name}")
async def get_table(request: Request, data=Depends(create_table)):
    """
    Обработка маршрута для отображения таблицы

    Параметры:
    --------------
    request: Request
        Объект запроса FastAPI
    data
        Параметр данных, получаемых из зависимости create_table
    
    Возвращает шаблон страницы с таблицей
    """
    return templates.TemplateResponse("table.html", {"request": request, "data": data})
