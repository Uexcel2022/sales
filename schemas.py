from datetime import datetime
from pydantic import BaseModel, EmailStr,Field
from models import ShipmentStatus

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(gt=0, le=25, description='Weight in KG')
    destination: int


class ShipmentRead(BaseShipment):
    id: int = Field(gt=0)
    status: ShipmentStatus
    estimated_delivery: datetime

class CreateShipment(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field( default=None,description='Number of days time.')


class CreateSeller(BaseModel):
    name: str = Field(pattern="^[a-zA-Z]{3,20} ?[a-zA-Z]*$")
    email: EmailStr
    password:str=Field(min_length=6,max_length=16)

class SellerRead(BaseModel):
    id: int
    name: str = Field(pattern="^[a-zA-Z]{3,20} ?[a-zA-Z]*$")
    email: EmailStr


class Token(BaseModel):
    access_token: str
    type: str

