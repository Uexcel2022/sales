from datetime import datetime
from pydantic import BaseModel,Field
from models import ShipmentStatus

class BaseShipment(BaseModel):
    content: str 
    weigth: float = Field(gt=0, le=25,description='Weight in KG')
    destination: int 
    

class ShipmentResponse(BaseShipment):
    id: int = Field(gt=0)
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentRequest(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field( default=None,description='Number of days time.')

