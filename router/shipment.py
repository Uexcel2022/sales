from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter,status,HTTPException
from sqlalchemy import select
from session import sesseionDep

from models import Shipment, ShipmentStatus
from schema import ShipmentRequest, ShipmentResponse, ShipmentUpdate
from service.shipment import ShipmentService

router = APIRouter(
    prefix="/api/v1",
    tags=["Shipment"],
)


@router.post('/shipments',status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment_data: ShipmentRequest, session: sesseionDep):
     shipment_service = ShipmentService(session)
     return await shipment_service.create(shipment_data)


@router.get('/shipment/{id}',response_model=ShipmentResponse,status_code=status.HTTP_200_OK)
async def read_one_shipment(id:int,session:sesseionDep):
    shipment_service = ShipmentService(session)
    return await shipment_service.read_one(id)


@router.get("/shipents", response_model=List[ShipmentResponse],status_code=status.HTTP_200_OK)
async def read_all_shipment(session: sesseionDep):
    shipment_service = ShipmentService(session)
    return await shipment_service.get_all()


@router.put("/shipments/{id}", status_code=status.HTTP_200_OK,response_model=ShipmentResponse)
async def update_shipment(session:sesseionDep,shipment_data:ShipmentUpdate,id:int):
    shipment_service = ShipmentService(session)
    return await shipment_service.update(shipment_data,id)


@router.delete("/shipments/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(session: sesseionDep,id:int):
  shipment_service = ShipmentService(session)
  await shipment_service.delete(id)
  
