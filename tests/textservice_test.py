from  services.text_service import TextService
from data.database_service import Databaseservice
from config import settings
import pytest


db_serv = Databaseservice(settings.DATABASE_URL_asyncpg)
text_service = TextService("", db_serv)

@pytest.mark.parametrize('text, spec_chars, result',
                         [("Hello, word \nYou win!?", [",", "!", "?", "\n"], "Hello word You win")])
def test_remove_chars_from_text(text, spec_chars, result):
    assert text_service.remove_chars_from_text(text, spec_chars) == result


@pytest.mark.parametrize('length_text, count_word, tf',
                         [(8, 2, 0.25),
                          (5, 1, 0.2),
                          (0, 0, 0)])
def test_get_tf(length_text, count_word, tf):
    assert abs(text_service.get_tf(length_text, count_word) - tf) < 0.00001


@pytest.mark.asyncio
async def test_create_tf():
    doc_id = 'test_id'
    word = 'test_word'
    tf = 0.7
    created_tf_instance = await text_service.create_tf(doc_id, word, tf)
    assert created_tf_instance is not None



    