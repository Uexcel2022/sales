from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter,status,HTTPException
from sqlalchemy import select
from session import sesseionDep

from models import Shipment, ShipmentStatus
from schema import ShipmentRequest, ShipmentResponse, ShipmentUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Shipment"],
)


@router.post('/shipments')
async def create_shipment(req: ShipmentRequest, session: sesseionDep,status_code=status.HTTP_201_CREATED):

    shipment = Shipment(
        **req.model_dump(),
        status= ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5)
        )
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return {"id":shipment.id}


@router.get('/shipment/{id}',response_model=ShipmentResponse,status_code=status.HTTP_200_OK)
async def read_one_shipment(id:int,session:sesseionDep):
    shipment = await session.get(Shipment,id)
    if(shipment is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shipment not found.')
    return shipment

@router.get("/shipents", response_model=List[ShipmentResponse],status_code=status.HTTP_200_OK)
async def read_all_shipment(session: sesseionDep):
    shipments = await session.scalars(select(Shipment))
    shipmentList = shipments.all()
    if len(shipmentList) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No shipment found.")
    return shipmentList


@router.put("/shipments/{id}", status_code=status.HTTP_200_OK,response_model=ShipmentResponse)
async def update_shipment(session:sesseionDep,req:ShipmentUpdate,id:int):
    shipment_data = req.model_dump(exclude_none=True)
    if shipment_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No data provided fro update.')
    
    topUdate = await session.get(Shipment,id) 

    if(topUdate is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shipment not found.')
    
    topUdate.sqlmodel_update(shipment_data)

    session.add(topUdate)
    await session.commit()
    await session.refresh(topUdate)
    return topUdate


@router.delete("/shipments/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(session: sesseionDep,id:int):
  shipment = session.get(Shipment,id)
  if shipment is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found.")
  await session.delete(shipment)
  await session.commit()
