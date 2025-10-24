
from typing import List
from fastapi import APIRouter,status
from dependency import shipmentServiceDep
from schemas import CreateShipment, ShipmentRead, ShipmentUpdate


router = APIRouter(
    prefix="/api/v1",
    tags=["Shipment"],
)


@router.post('/shipments',status_code=status.HTTP_201_CREATED,response_model=ShipmentRead)
async def create_shipment(shipment_data: CreateShipment, service:shipmentServiceDep):
     return await service.create(shipment_data)
     
     
@router.get('/shipment/{id}',response_model=ShipmentRead,status_code=status.HTTP_200_OK)
async def read_one_shipment(id:int,service: shipmentServiceDep):
    return  await service.read_one(id)


@router.get("/shipents", response_model=List[ShipmentRead],status_code=status.HTTP_200_OK)
async def read_all_shipment(service: shipmentServiceDep):
    return await service.get_all()
    


@router.put("/shipments/{id}", status_code=status.HTTP_200_OK,response_model=ShipmentRead)
async def update_shipment(service:shipmentServiceDep,shipment_data:ShipmentUpdate,id:int):
    return await service.update(shipment_data,id)



@router.delete("/shipments/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(service:shipmentServiceDep,id:int):
  await service.delete(id)
  
