from .database_service import Base
from sqlalchemy.orm import Mapped, mapped_column

class Tf(Base):
    __tablename__ = 'Tf'

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[str]
    word: Mapped[str]
    tf: Mapped[float]


class Idf(Base):
    __tablename__ = 'Idf'

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] 
    idf: Mapped[float]
    