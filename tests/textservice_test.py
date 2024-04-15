from  services.text_service import TextService
from data.database_service import Databaseservice
from config import settings
from math import log
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


@pytest.mark.asyncio
async def test_count_doc():
    data = [{"doc_id": "one", "word": "test1", "tf": 0.3},
            {"doc_id": "two", "word": "test2", "tf": 0.55},
            {"doc_id": "three", "word": "test3", "tf": 0.72},
            {"doc_id": "four", "word": "test3", "tf": 0.19},
            {"doc_id": "five", "word": "test5", "tf": 0.49}]
    for note in data:
        await text_service.create_tf(note["doc_id"], note["word"], note["tf"])
    assert await text_service.count_doc() == len(data)



@pytest.mark.asyncio
async def test_count_doc_word():
    assert await text_service.count_doc_word("test1") == 1



@pytest.mark.asyncio
async def test_get_idf():
    count_doc = 5 # len(data) in test_count_doc
    count_doc_word = 2 # word test3
    delit = count_doc / count_doc_word
    idf = log(delit)
    assert abs(await text_service.get_idf("test3") - idf) < 0.00001

    
@pytest.mark.asyncio
async def test_create_idf():
    created_idf_instance = await text_service.create_idf("test3")
    assert created_idf_instance is not None


@pytest.mark.asyncio
async def test_check_idf():
    assert await text_service.check_idf("test3") is not None
    assert await text_service.check_idf("word") is False

