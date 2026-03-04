from pydantic import BaseModel, Field, ConfigDict


class AddressCreate(BaseModel):
    name: str = Field()
    street: str
    city: str
    latitude: float
    longitude: float


class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class AddressResponse(AddressCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)