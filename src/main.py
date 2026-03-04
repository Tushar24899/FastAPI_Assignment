from contextlib import asynccontextmanager

from fastapi import FastAPI

from address_book_api.api.api_router import router
from address_book_api.db.db import engine
from address_book_api.models.address import Base

app = FastAPI()

app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables at startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield