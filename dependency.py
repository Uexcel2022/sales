
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from service.auth import AuthService
from service.shipment import ShipmentService
from session import get_session
from fastapi import Depends


sesseionDep = Annotated[AsyncSession,Depends(get_session)]

def get_shipment_service(session:sesseionDep):
    return ShipmentService(session)

def get_seller_service(session:sesseionDep):
    return AuthService(session)


shipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

sellerServiceDep = Annotated[AuthService, Depends(get_seller_service)]
