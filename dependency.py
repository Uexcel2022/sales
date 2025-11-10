
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from service.seller import SellerService
from service.shipment import ShipmentService
from service.delivary_partner import DeliverPartnerService
from session import get_session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

pwd_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/seller/token")

sesseionDep = Annotated[AsyncSession,Depends(get_session)]

def get_shipment_service(session:sesseionDep):
    return ShipmentService(session)

def get_seller_service(session:sesseionDep):
    return SellerService(session)

def get_delivery_partner_service(session:sesseionDep):
    return DeliverPartnerService(session)




shipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

deliveryPartnerServiceDep = Annotated[DeliverPartnerService, Depends(get_delivery_partner_service)]

sellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

pwd_bearerDP = Annotated[str, Depends(pwd_bearer)]


