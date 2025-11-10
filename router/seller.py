from typing import Annotated
from fastapi import APIRouter, Depends,status
from dependency import sellerServiceDep,pwd_bearerDP
from schemas import CreateSeller, LoggedOut, SellerRead, Token
from fastapi.security import OAuth2PasswordRequestForm


 
router = APIRouter(
    prefix="/api/v1",
    tags=["Seller"]
)

@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=SellerRead)
async def register_seller(seller:CreateSeller, service:sellerServiceDep):
    return await service.create(seller)

@router.get("/seller",response_model=SellerRead)
async def get_logged_in_seller(service:sellerServiceDep,token:pwd_bearerDP):
    return await service.token_validation(token)

@router.post("/seller/token", status_code=status.HTTP_200_OK,response_model=Token)
async def authenticate_seller(service:sellerServiceDep,form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    token = await service.authenticate_seller(form_data.username,form_data.password)
    return {"access_token": token, "type":"jwt"}

@router.post("/logout",response_model=LoggedOut)
async def logout_handler(token: pwd_bearerDP, service:sellerServiceDep):

    return await service.logout(token)