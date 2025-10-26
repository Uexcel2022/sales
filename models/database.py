from pydantic import EmailStr
from sqlmodel import SQLModel,Field,Session
from enum import Enum
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed="placed"
    in_transit = "in_transit"
    out_for_delivery= "out_for_delivery"
    delivered="delivered"

class Shipment(SQLModel,table=True):
    __tablename__ ='shipment'
    id: int = Field(primary_key= True)
    content: str 
    weight: float = Field(..., gt=0, le=25)
    destination: int 
    status: ShipmentStatus 
    estimated_delivery: datetime


class Seller(SQLModel,table=True):
    __tablename__ ="seller"
    id: int = Field(primary_key=True)
    name: str = Field(regex="^[a-zA-Z]* ?[a-zA-Z]{3,15}$")
    email: EmailStr=Field(unique= True)
    hashed_password:str

    def model_dump(self):
        return {
            "id":self.id,
            "name":self.name,
            "email": self.email
        }
