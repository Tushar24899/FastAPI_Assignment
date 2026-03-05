from fastapi import APIRouter, Depends, HTTPException, status

from address_book_api.db.db import get_address_service
from address_book_api.schema.address import AddressCreate, AddressUpdate
from address_book_api.service.address import AddressService
from resources.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new address",
    description="Creates a new address entry in the address book."
)
async def create_address(
    data: AddressCreate,
    service: AddressService = Depends(get_address_service),
):
    logger.info(
        "Received request to create address",
        extra={"city": data.city, "street": data.street}
    )

    try:
        address = await service.create_address(data)

        logger.info(
            "Address created successfully",
            extra={"address_id": address.id}
        )

        return address

    except Exception as e:
        logger.error(
            "Failed to create address",
            extra={"error": str(e)},
            exc_info=True
        )
        raise


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all addresses",
    description="Retrieves all addresses stored in the address book."
)
async def list_addresses(
    service: AddressService = Depends(get_address_service),
):
    logger.info("Fetching all addresses")

    try:
        addresses = await service.get_addresses()

        logger.info(
            "Fetched addresses successfully",
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


@router.put(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    summary="Update an address",
    description="Updates an existing address using the provided address ID."
)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    service: AddressService = Depends(get_address_service),
):

    logger.info(
        "Updating address",
        extra={"address_id": address_id}
    )

    try:
        updated = await service.update_address(
            address_id,
            data.dict(exclude_unset=True),
        )

        if not updated:
            logger.warning(
                "Address not found for update",
                extra={"address_id": address_id}
            )
            raise HTTPException(status_code=404, detail="Address not found")

        logger.info(
            "Address updated successfully",
            extra={"address_id": address_id}
        )

        return updated

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            "Failed to update address",
            extra={"address_id": address_id, "error": str(e)},
            exc_info=True
        )
        raise


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an address",
    description="Deletes an address from the address book using the address ID."
)
async def delete_address(
    address_id: int,
    service: AddressService = Depends(get_address_service),
):

    logger.info(
        "Deleting address",
        extra={"address_id": address_id}
    )

    try:
        deleted = await service.delete_address(address_id)

        if not deleted:
            logger.warning(
                "Address not found for deletion",
                extra={"address_id": address_id}
            )
            raise HTTPException(status_code=404, detail="Address not found")

        logger.info(
            "Address deleted successfully",
            extra={"address_id": address_id}
        )

        return {"message": "Address deleted"}

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            "Failed to delete address",
            extra={"address_id": address_id, "error": str(e)},
            exc_info=True
        )
        raise


@router.get(
    "/nearby",
    status_code=status.HTTP_200_OK,
    summary="Find nearby addresses",
    description="Returns all addresses within a specified distance (in kilometers) from the provided latitude and longitude."
)
async def get_nearby_addresses(
    latitude: float,
    longitude: float,
    distance_km: float,
    service: AddressService = Depends(get_address_service),
):

    logger.info(
        "Fetching nearby addresses",
        extra={
            "latitude": latitude,
            "longitude": longitude,
            "distance_km": distance_km
        }
    )

    try:
        addresses = await service.get_nearby_addresses(
            latitude,
            longitude,
            distance_km
        )

        logger.info(
            "Nearby addresses fetched successfully",
            extra={"count": len(addresses)}
        )

        return addresses

    except Exception as e:

        logger.error(
            "Error fetching nearby addresses",
            extra={
                "latitude": latitude,
                "longitude": longitude,
                "distance_km": distance_km,
                "error": str(e)
            },
            exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch nearby addresses"
        )