import string
from fastapi import UploadFile
from collections import Counter
from sqlalchemy import select, distinct, func
import uuid
from math import log
from data.database_service import Databaseservice
from data.models import Tf, Idf
from .table_service import TableService

class TextService:
    """
    Класс TextService реализует работу с текстом, загруженного файла

    Note:
        Есть проблемы с кодировкой Windows
    
    Атрибуты:
    ------------
    content: bytes
        Содержание, загружаемого файла
    database_service: Databaseservice
        Сервис базы данных

    Методы:
    ------------
    remove_chars_from_text(text, spec_chars)
        Очистка текста, от специальных символов.
        Возвращает очищенный текст
    
    get_tf(length_text, count_word)
        Вычисление tf для определенного слова
        Возвращает tf как float
    
    generate_doc_id()
        Генерация id для документа
        Возвращает doc_id в виде строки

    create_tf(doc_id, word, tf)
        Создание новой записи модели Tf в базу данных

    count_doc()
        Осуществление запроса в БД
        Возвращает количество документов в коллекции
    
    count_doc_word(word)
        Осуществление запроса в БД
        Возвращает количество документов, в которых 
        содержится определенное слово

    get_idf(word)
        Вычисление idf для определенного слова
        Вовращает idf типа float
    
    check_idf(word)
        Проверка наличия idf в бд для определенного слова
        Возвращает либо False, либо найденное idf

    create_idf(word)
        Создание новой записи модели idf в бд
    
    update_idf(id, word)
        Обновление значения idf в бд для заданного слова
    
    preprocessing()
        Декодирование текста файла и его очистка
        Возвращает очищенный текст

    processing()
        Обработка текста файла
        Возвращает 50 слов документа с посчитанными tf, idf
    """

    def __init__(self, content, database_service: Databaseservice):
        self.database_service = database_service
        self.content = content


    def remove_chars_from_text(self, text, spec_chars):
            """
            Очистка текста от специальных символов

            Параметры:
            ------------
            text: str
                Текст для очистки
            spec_shars: list
                Список специальных символов
            """

            return "".join([str(ch) for ch in text if str(ch) not in spec_chars])

    
    def get_tf(self, length_text, count_word):
        """
        Подсчет tf для определенного слова

        Параметры:
        ------------
        lenght_text: int
            Длина текста в загруженном документе
        count_word: int
            Количество вхождений слова в текст
        """
        try:
            tf = count_word / length_text
        except ZeroDivisionError:
            return 0
        return tf
    

    def generate_doc_id(self):
        """
        Генерация id для загруженного документа
        """

        doc_id = uuid.uuid4()
        return str(doc_id)


    async def create_tf(self, doc_id: str, word: str, tf: float):
        """
        Создание записи в бд в таблице Tf

        Параметры:
        ------------
        doc_id: str
            id документа
        word: str
            Определенное слово
        tf: float
            tf для заданного слова
        """

        created_tf = Tf(doc_id=doc_id, word=word, tf=tf)
        return await self.database_service.save(instance=created_tf)
    

    async def count_doc(self):
        """
        Запрос в бд для получения количества документов в коллекции
        """

        query = select(func.count(distinct(Tf.doc_id)))
        return await self.database_service._first(query)
    

    async def count_doc_word(self, word):
        """
        Запрос в бд для получения количества документов,
        содержащих заданное слово

        Параметр:
        -----------
        word: str
            Заданное слово
        """

        query = select(func.count(distinct(Tf.doc_id))).where(Tf.word == word)
        return await self.database_service._first(query)
    

    async def get_idf(self, word):
        """
        Подсчет idf для заданного слова

        Параметр:
        --------------
        word: str
            Заданное слово
        """

        count_doc = await self.count_doc()
        сount_doc_word = await self.count_doc_word(word)
        deli = count_doc / сount_doc_word
        idf = log(deli)
        return idf


    async def check_idf(self, word):
        """
        Запрос в бд, для проверки наличия idf для заданного слова

        Парамет:
        ---------------
        word: str
            Заданное слово
        """

        query = select(Idf.id).where(Idf.word == word)
        respond = await self.database_service._first(query)
        if respond is None:
            return False
        return respond


    async def create_idf(self, word: str):
        """
        Создание новой записи в бд в таблице Idf для заданного слова

        Параметр:
        word: str
            Заданное слово
        """

        idf = await self.get_idf(word)
        created_idf = Idf(word=word, idf=idf)
        return await self.database_service.save(instance=created_idf)


    async def update_idf(self, id, word):
        """
        Обновление записи в таблице Idf заданного слова

        Параметр:
        word: str
            Заданное слово
        """

        session = self.database_service.session
        need_word = await session.get(Idf, id)
        need_word.idf = await self.get_idf(word)
        await session.commit()
    

    def preprocessing(self):
        """
        Очистка текста от специальных символов и 
        приведение к 1 регистру
        """

        contents = self.content.decode()
        contents = contents.lower()
        contents = self.remove_chars_from_text(contents, string.punctuation)
        return contents
    
    async def processing(self):
        """
        Обработка текста файла
        """

        content = self.preprocessing()
        text = content.split()
        length = len(text)
        doc_id = self.generate_doc_id()
        count_word = Counter(text)
        for word, count in count_word.items():
            tf = self.get_tf(length, count)
            await self.create_tf(doc_id, word, tf)
            res_chec = await self.check_idf(word)
            if res_chec == False:
                await self.create_idf(word)
            else:
                await self.update_idf(res_chec, word)
        tb = TableService(doc_id, self.database_service)
        return await tb.choice50() 
    