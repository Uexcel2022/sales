from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from models.database import ShipmentStatus

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(gt=0, le=25, description='Weight in KG')
    destination: int


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
    def model_dump(self):
        return{
            "id":self.id,
            "name":self.name,
            "email": self.email
        }



class ShipmentRead(BaseShipment):
    id: int = Field(gt=0)
    status: ShipmentStatus
    estimated_delivery: datetime
    seller: Optional[SellerRead]=Field(default=None)

    def model_dump(self):
        return{
            "content":self.content,
            "status":self.status,
            "estimated_delivery": self.estimated_deliver,
            "seller": self.seller.model_dump()
        }
        
class LoggedOut(BaseModel):
    message: str = Field( default="You have been logged out successfully!")




class Token(BaseModel):
    access_token: str
    type: str

