from fastapi import APIRouter
from address_book_api.api.routes import address_book

router = APIRouter()

router.include_router(
    address_book.router,
    prefix="/addresses",
    tags=["Address Book"]
)