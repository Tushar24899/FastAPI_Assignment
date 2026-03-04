from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from address_book_api.db.repository.address_repository import AddressRepository
from address_book_api.service.address import AddressService
from resources.logging_config import get_logger

logger = get_logger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./addresses.db"

engine = create_async_engine(DATABASE_URL)

SessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False
)


# ---------------------------
# Database Dependency
# ---------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Create database session using DI"""

    logger.debug("Creating database session")

    async with SessionFactory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(
                "Error in database session",
                extra={"error": str(e)},
                exc_info=True,
            )
            await session.rollback()
            raise
        finally:
            logger.debug("Closing database session")
            await session.close()


# ---------------------------
# Repository Dependency
# ---------------------------
async def get_address_repo(
    db: AsyncSession = Depends(get_db),
) -> AddressRepository:

    logger.debug("Creating AddressRepository instance")

    return AddressRepository(db)


# ---------------------------
# Service Dependency
# ---------------------------
async def get_address_service(
    repo: AddressRepository = Depends(get_address_repo),
) -> AddressService:

    logger.debug("Creating AddressService instance")

    return AddressService(repo)