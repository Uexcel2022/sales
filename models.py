from sqlmodel import SQLModel,Field,Session
from enum import Enum
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed='placed'
    in_transit = 'in_transit'
    out_for_delivary= 'out_for_delivary'
    delivered='delivered'


class Shipment(SQLModel,table=True):
    __tablename__ ='shipment'
    id: int = Field(primary_key= True)
    content: str 
    weigth: float = Field(gt=0, le=25)
    destination: int 
    status: ShipmentStatus 
    estimated_delivery: datetime

