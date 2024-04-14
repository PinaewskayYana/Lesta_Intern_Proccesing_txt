from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import Optional, Sequence, Any


class Base(DeclarativeBase):
    """
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
    """

class Databaseservice:
    """
    Класс для работы с базой данных

    Методы:
    ---------
    start()
        Инициализация соединения с бд и создание сессии для работы

    stor()
        Закрытие соединения с бд

    _first(query): Optional[Any]
        Выполнение запроса к бд
        Запрос передается в параметре query
        Возвращает первый результат запроса, если он существует

    _all(self, query, unpack): Sequence[Any]
        Выполнение запроса к бд
        Запрос передается в параметре query
        Возвращает все результаты запроса

    save(self, instance: Base): Base
        Сохранение экземпляра, переданного в параметре instance

    init_meta_data(self):
        Создание все таблиц, описанных ORM моделями Base

    """
    
    def __init__(self, dns: str):
        self.engine = create_async_engine(url=dns,
                                    echo=True, future=True)
        self.session: Optional[AsyncSession] = None
        self.session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)()

    async def start(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self.session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)()
    

    async def stop(self):
        await self.session.close()
        self.session = None

    
    async def _first(self, query) -> Optional[Any]:
        result = (await self.session.execute(query)).first() or []
        if result:
            return result[0]
        

    async def _all(self, query, unpack: bool = False) -> Sequence[Any]:
        results = (await self.session.execute(query)).all() or []
        if unpack:
            results = [result[0] for result in results]
        return results
    

    async def save(self, instance: Base) -> Base:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


    async def init_meta_data(self):
        Base.metadata.create_all(self.engine)
    

