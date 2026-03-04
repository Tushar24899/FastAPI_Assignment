from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from address_book_api.models.address import AddressBook
from resources.logging_config import get_logger

logger = get_logger(__name__)


class AddressRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_address(self, address: AddressBook):

        logger.info(
            "Creating address in database",
            extra={"city": address.city, "street": address.street}
        )

        try:
            self.db.add(address)

            await self.db.commit()

            await self.db.refresh(address)

            logger.info(
                "Address created successfully",
                extra={"address_id": address.id}
            )

            return address

        except Exception as e:

            logger.error(
                "Database error while creating address",
                extra={"error": str(e)},
                exc_info=True
            )

            await self.db.rollback()

            raise

    async def get_all(self):

        logger.debug("Fetching all addresses from database")

        try:
            stmt = select(AddressBook)

            result = await self.db.execute(stmt)

            addresses = result.scalars().all()

            logger.info(
                "Addresses fetched successfully",
                extra={"count": len(addresses)}
            )

            return addresses

        except Exception as e:

            logger.error(
                "Database error while fetching addresses",
                extra={"error": str(e)},
                exc_info=True
            )

            raise

    async def update_address(self, address_id: int, data: dict):

        logger.info(
            "Updating address in database",
            extra={"address_id": address_id}
        )

        try:
            stmt = select(AddressBook).where(AddressBook.id == address_id)

            result = await self.db.execute(stmt)

            address = result.scalar_one_or_none()

            if not address:
                logger.warning(
                    "Address not found for update",
                    extra={"address_id": address_id}
                )
                return None

            for key, value in data.items():
                setattr(address, key, value)

            await self.db.commit()

            await self.db.refresh(address)

            logger.info(
                "Address updated successfully",
                extra={"address_id": address_id}
            )

            return address

        except Exception as e:

            logger.error(
                "Database error while updating address",
                extra={"address_id": address_id, "error": str(e)},
                exc_info=True
            )

            await self.db.rollback()

            raise

    async def delete_address(self, address_id: int):

        logger.info(
            "Deleting address from database",
            extra={"address_id": address_id}
        )

        try:
            stmt = select(AddressBook).where(AddressBook.id == address_id)

            result = await self.db.execute(stmt)

            address = result.scalar_one_or_none()

            if not address:
                logger.warning(
                    "Address not found for deletion",
                    extra={"address_id": address_id}
                )
                return None

            await self.db.delete(address)

            await self.db.commit()

            logger.info(
                "Address deleted successfully",
                extra={"address_id": address_id}
            )

            return address

        except Exception as e:

            logger.error(
                "Database error while deleting address",
                extra={"address_id": address_id, "error": str(e)},
                exc_info=True
            )

            await self.db.rollback()

            raise