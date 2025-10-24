from typing import Annotated
from fastapi import APIRouter, Depends,status
from dependency import sellerServiceDep
from schemas import CreateSeller, SellerRead, Token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

pwd_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
 
router = APIRouter(
    prefix="/api/v1",
    tags=["Seller"]
)

@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=SellerRead)
async def register_seller(seller:CreateSeller, service:sellerServiceDep):
    return await service.create(seller)

@router.get("/seller/{id}",response_model=SellerRead)
async def get_seller(id:int, service:sellerServiceDep):
    return await service.get_seller(id)

@router.post("/token", status_code=status.HTTP_200_OK,response_model=Token)
async def authenticate_seller(service:sellerServiceDep,form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    token = await service.authenticate_seller(form_data.username,form_data.password)
    return {"access_token": token, "type":"jwt"}

@router.post("/dashboard")
async def seller_dashboard(token: Annotated[str, Depends(pwd_bearer)]):
    return {"token":token}