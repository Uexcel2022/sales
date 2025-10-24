
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,status
from typing import Any, Optional, Dict

import jwt
from config import sec_settings

from sqlalchemy import select
from models import Seller
from schemas import CreateSeller
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
 


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,seller:CreateSeller)->Dict[str, Any]:
        new_seller = Seller(
            **seller.model_dump(exclude={'password'}),
            hashed_password=pwd_context.hash(seller.password)
        )
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        return new_seller.model_dump()
    
    async def get_seller(self, id:int)->Dict[str, Any]:
        seller: Optional[Seller] = await self.session.get(Seller, id)
        if not seller:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Seller not found") 
        return seller.model_dump()
    

    async def authenticate_seller(self, email, password)->str:
        
        # result = await self.session.scalars(select(Seller).filter_by(email=email))
        # seller = result.one_or_none()
        
        result = await self.session.execute(select(Seller).where(Seller.email == email))

        seller = result.scalar()

        if not seller or not pwd_context.verify(password, seller.hashed_password):

            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password!")
        
        token = jwt.encode(
            payload={
                "user": {
                "id": seller.id,
                "name": seller.name
            },"exp": datetime.now(timezone.utc)+ timedelta(days=1),
        }, algorithm=sec_settings.ALGORITHM,key=sec_settings.SECRET_KEY)

        return token
    
   



    