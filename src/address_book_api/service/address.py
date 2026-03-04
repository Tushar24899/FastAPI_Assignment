from geopy.distance import geodesic

from address_book_api.db.repository.address_repository import AddressRepository
from address_book_api.models.address import AddressBook
from address_book_api.schema.address import AddressCreate
from resources.logging_config import get_logger

logger = get_logger(__name__)


class AddressService:

    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def create_address(self, data: AddressCreate):

        logger.info(
            "Creating address",
            extra={"city": data.city, "street": data.street}
        )

        try:
            address = AddressBook(
                name=data.name,
                street=data.street,
                city=data.city,
                latitude=data.latitude,
                longitude=data.longitude,
            )

            result = await self.repo.create_address(address)

            logger.info(
                "Address created successfully",
                extra={"address_id": result.id}
            )

            return result

        except Exception as e:
            logger.error(
                "Failed to create address",
                extra={"error": str(e)},
                exc_info=True
            )
            raise

    async def get_addresses(self):

        logger.info("Fetching all addresses")

        try:
            addresses = await self.repo.get_all()

            logger.info(
                "Addresses fetched successfully",
                extra={"count": len(addresses)}
            )

            return addresses

        except Exception as e:
            logger.error(
                "Failed to fetch addresses",
                extra={"error": str(e)},
                exc_info=True
            )
            raise

    async def update_address(self, address_id: int, data):

        logger.info(
            "Updating address",
            extra={"address_id": address_id}
        )

        try:
            updated = await self.repo.update_address(address_id, data)

            if not updated:
                logger.warning(
                    "Address not found for update",
                    extra={"address_id": address_id}
                )

            return updated

        except Exception as e:
            logger.error(
                "Failed to update address",
                extra={"address_id": address_id, "error": str(e)},
                exc_info=True
            )
            raise

    async def delete_address(self, address_id: int):

        logger.info(
            "Deleting address",
            extra={"address_id": address_id}
        )

        try:
            deleted = await self.repo.delete_address(address_id)

            if not deleted:
                logger.warning(
                    "Address not found for deletion",
                    extra={"address_id": address_id}
                )

            return deleted

        except Exception as e:
            logger.error(
                "Failed to delete address",
                extra={"address_id": address_id, "error": str(e)},
                exc_info=True
            )
            raise

    async def get_nearby_addresses(self, latitude: float, longitude: float, distance_km: float):

        logger.info(
            "Finding nearby addresses",
            extra={
                "latitude": latitude,
                "longitude": longitude,
                "distance_km": distance_km
            }
        )

        try:
            addresses = await self.repo.get_all()

            user_location = (latitude, longitude)

            nearby = []

            for addr in addresses:

                addr_location = (addr.latitude, addr.longitude)

                if geodesic(user_location, addr_location).km <= distance_km:
                    nearby.append(addr)

            logger.info(
                "Nearby addresses found",
                extra={"count": len(nearby)}
            )

            return nearby

        except Exception as e:
            logger.error(
                "Error finding nearby addresses",
                extra={"error": str(e)},
                exc_info=True
            )
            raise