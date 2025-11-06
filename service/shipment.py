from typing import Optional, Sequence
from fastapi import HTTPException,status
from sqlalchemy import select
from models.database import Shipment, ShipmentStatus
from schemas import CreateShipment, ShipmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timedelta
from uuid import UUID


class ShipmentService:
    def __init__(self,session:AsyncSession):
        self.session = session
    
    async def commit(self,shipment:Shipment):
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
    

    async def create(self,shipment_data:CreateShipment,id:UUID)->Shipment:
        new_shipment = Shipment(
        **shipment_data.model_dump(),
        status= ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=5),
        seller_id= id
        )
        await self.commit(new_shipment)
        return new_shipment

    async def read_one(self,id:UUID)->Shipment:
        shipment: Optional[Shipment] = await self.session.get(Shipment,id)
        if not shipment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shipment not found.')
        return shipment
    
    async def read_all_seller_shipments(self,id:UUID)->Sequence[Shipment]:
        result = await self.session.scalars(select(Shipment).filter_by(seller_id=id))
        shipments = result.all()
        
        if len(shipments) ==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No shipment found.')
        return shipments

    async def update(self,shipment_data:ShipmentUpdate,id:UUID):
        shipment =  await self.read_one(id)
        update = shipment_data.model_dump(exclude_none=True)
        if not update:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No data provided for update.')
        shipment.sqlmodel_update(update)
        await self.commit(shipment)
        return shipment

    async def get_all(self):
        shipments = await self.session.scalars(select(Shipment))
        shipmentList = shipments.all()
        if len(shipmentList) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No shipment found.")
        return shipmentList
    
    async def delete(self,id:UUID)->None:
        shipment = await self.read_one(id)
        await self.session.delete(shipment)
        await self.session.commit()

    

        



