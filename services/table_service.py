from sqlalchemy import select, distinct, func
from math import log
from data.database_service import Databaseservice
from data.models import Tf, Idf

class TableService:
    """
    Класс для получения 50 слов из загруженного документа
    В виде (id, word, tf, idf)

    Атрибуты:
    --------------
    doc_id: str
        id необходимого документа
    database_service: Databaseservice
        Сервис базы данных

    Метод:
    -------------
    choice50()
        Запрос в бд
        Возвращения 50 слов
    """

    def __init__(self, doc_id: str, database_service: Databaseservice):
        self.doc_id = doc_id
        self.database_service = database_service


    async def choice50(self):
        query = select(func.row_number().over(order_by=Tf.word).label("id"), Tf.word, Tf.tf, Idf.idf).join(
            Idf, Tf.word == Idf.word
        ).filter(Tf.doc_id == self.doc_id).order_by(
            Idf.idf.desc()
        ).limit(50)
        res = await self.database_service._all(query)
        dtc = [{"id": index+1, "word": item[1], "tf": item[2], "idf": item[3]} for index, item in enumerate(res)]
        return dtc