from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends,status
from dependency import deliveryPartnerServiceDep as dpServiceDep
from schemas import DeliveryPartnerCreate,DeliveryPartnerRead, Token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm as authForm
pwd_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/delivery_partner/token")
pwdb_bearerDep = Annotated[str, Depends(pwd_bearer)]

router = APIRouter(
    prefix= "/api/v1",
    tags= ["Delivery Partner"]

)

@router.post("/signup",response_model=DeliveryPartnerRead,status_code=status.HTTP_201_CREATED)
async def create_delivery_partner(service:dpServiceDep,dp:DeliveryPartnerCreate):
   return await service.create(dp)

@router.get("/deliver_partner/{id}",response_model=DeliveryPartnerRead,status_code=status.HTTP_200_OK)
async def get_delivery_partner(service:dpServiceDep,id:UUID):
    return await service.get_delivery_partner(id)

@router.post("/delivery_partner/token",status_code=status.HTTP_200_OK,response_model=Token)
async def authenticate_delivery_partner(auth_form: Annotated[authForm, Depends()], service:dpServiceDep):
    return await service.authenticate_delivery_partner(auth_form.username,auth_form.password)