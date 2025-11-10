
from typing import List
from uuid import UUID
from fastapi import APIRouter,status
from dependency import shipmentServiceDep,sellerServiceDep,pwd_bearerDP
from schemas import CreateShipment, ShipmentRead, ShipmentUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Shipment"],
)


@router.post('/shipments',status_code=status.HTTP_201_CREATED,response_model=ShipmentRead)
async def create_shipment(token:pwd_bearerDP,shipment_data: CreateShipment,
                          service:shipmentServiceDep,auth:sellerServiceDep):
     seller = await auth.token_validation(token)
     shpiment = await service.create(shipment_data, seller['id'])
     return shpiment


@router.get('/seller/shipments',response_model=List[ShipmentRead],status_code=status.HTTP_200_OK)
async def read_seller_shipments(token:pwd_bearerDP,id:UUID,
                            service: shipmentServiceDep,authService:sellerServiceDep):
    seller = await authService.token_validation(token)
    shipment = await service.read_all_seller_shipments(seller['id'])
    return shipment
    
     
@router.get('/shipments/{id}',response_model=ShipmentRead,status_code=status.HTTP_200_OK)
async def read_one_shipment(token:pwd_bearerDP,id:UUID,
                            service: shipmentServiceDep,authService:sellerServiceDep):
    await authService.token_validation(token)
    shipment = await service.read_one(id)
    return shipment
    

@router.get("/shipents", response_model=List[ShipmentRead],status_code=status.HTTP_200_OK)
async def read_all_shipment(token:pwd_bearerDP,authService:sellerServiceDep,service: shipmentServiceDep):
    await authService.token_validation(token)
    return await service.get_all()
    

@router.put("/shipments/{id}", status_code=status.HTTP_200_OK,response_model=ShipmentRead)
async def update_shipment(authService:sellerServiceDep,token:pwd_bearerDP,
                          service:shipmentServiceDep,shipment_data:ShipmentUpdate,id:UUID):
    await authService.token_validation(token)
    return await service.update(shipment_data,id)


@router.delete("/shipments/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(authService:sellerServiceDep,token:pwd_bearerDP,service:shipmentServiceDep,id:UUID):
  await authService.token_validation(token)
  await service.delete(id)
  
