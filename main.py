import os
import sys
import asyncio

import uvicorn
from fastapi import FastAPI

from data.database_service import Databaseservice, Base
from services.service import APIService
from config import settings
from starlette.middleware.cors import CORSMiddleware


db_service = Databaseservice(settings.DATABASE_URL_asyncpg)

api = APIService(db_service)

@api.app.on_event("startup")
async def init_db():
    async with db_service.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

api.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app="main:api.app", reload=True)