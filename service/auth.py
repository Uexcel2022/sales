
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,status
from typing import Any, Optional
from uuid import uuid4
from models.redis import add_token_to_blacklist,is_token_blacklisted

import jwt
from config import sec_settings

from sqlalchemy import select
from models.database import Seller
from schemas import CreateSeller
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,seller:CreateSeller)->dict[str, Any]:
        new_seller = Seller(
            **seller.model_dump(exclude={'password'}),
            hashed_password=pwd_context.hash(seller.password)
        )
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        return new_seller.model_dump()
    
    async def get_seller(self, id:int)->dict[str, Any]:
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
                },
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc)+ timedelta(days=1)
            },
            algorithm=sec_settings.ALGORITHM,key=sec_settings.SECRET_KEY
        )

        return token
    

    async def token_validation(self,token:str)->dict[str,Any]:
            
            payload = await self.decode_token(token)

            if await is_token_blacklisted(payload['jti']):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed!")
        
            seller = await self.session.get(Seller,payload['user']['id'])
            if not seller:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Seller does not exist!")

            return seller.model_dump()
        

    async def decode_token(self,token)->dict[str,Any]:
         try:
            payload = jwt.decode(
                token,
                algorithms=[sec_settings.ALGORITHM],
                key=sec_settings.SECRET_KEY
            )

            return payload
        
         except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication failed!")
            

    async def logout(self, token:str):
        payload = await self.decode_token(token)
        token_id = payload['jti']

        await add_token_to_blacklist(token_id,(60*24*30*6))

        return {
            "detail": "You have been logged out successfully!"
        }