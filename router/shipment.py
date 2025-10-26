
from typing import List
from fastapi import APIRouter,status
from dependency import shipmentServiceDep,authServiceDep,pwd_bearerDP
from schemas import CreateShipment, ShipmentRead, ShipmentUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Shipment"],
)


@router.post('/shipments',status_code=status.HTTP_201_CREATED,response_model=ShipmentRead)
async def create_shipment(token:pwd_bearerDP,shipment_data: CreateShipment,
                          service:shipmentServiceDep,auth:authServiceDep):
     shpiment = await service.create(shipment_data)
     seller = await auth.token_validation(token)
     shipment_info = {**shpiment.model_dump()}
     shipment_info.update({"seller":seller})
     return shipment_info
    
     
     
@router.get('/shipments/{id}',response_model=ShipmentRead,status_code=status.HTTP_200_OK)
async def read_one_shipment(token:pwd_bearerDP,id:int,
                            service: shipmentServiceDep,authService:authServiceDep):
    seller = await authService.token_validation(token)
    shipment = await service.read_one(id)
    shipment_info = {**shipment.model_dump()}
    shipment_info.update({"seller":seller})
    return shipment_info
    

@router.get("/shipents", response_model=List[ShipmentRead],status_code=status.HTTP_200_OK)
async def read_all_shipment(token:pwd_bearerDP,authService:authServiceDep,service: shipmentServiceDep):
    await authService.token_validation(token)
    return await service.get_all()
    

@router.put("/shipments/{id}", status_code=status.HTTP_200_OK,response_model=ShipmentRead)
async def update_shipment(authService:authServiceDep,token:pwd_bearerDP,
                          service:shipmentServiceDep,shipment_data:ShipmentUpdate,id:int):
    await authService.token_validation(token)
    return await service.update(shipment_data,id)


@router.delete("/shipments/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(authService:authServiceDep,token:pwd_bearerDP,service:shipmentServiceDep,id:int):
  await authService.token_validation(token)
  await service.delete(id)
  
