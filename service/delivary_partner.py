from datetime import datetime, timedelta, timezone
from fastapi import HTTPException,status
from sqlmodel import select
from models.database import DeliveryPartner
from schemas import DeliveryPartnerCreate
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from uuid import UUID,uuid4
from config import sec_settings as sec

pwd_context = CryptContext(schemes=["bcrypt_sha256"],deprecated="auto")

import jwt

class DeliverPartnerService:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self, dp: DeliveryPartnerCreate):
        new_dp=DeliveryPartner(
            **dp.model_dump(exclude={"password"}),
             hashed_password= pwd_context.hash(dp.password),
         )
        self.session.add(new_dp)
        await self.session.commit()
        await self.session.refresh(new_dp)
        return new_dp
    
    async def get_delivery_partner(self, id:UUID):
        dp = await self.session.get(DeliveryPartner, id)
        if not dp:
            raise HTTPException(status_code=404, detail="Delivery Partner not found")
        return dp
    
    async def authenticate_delivery_partner(self, email:str, password:str)->dict[str,str]:
       result = await self.session.execute(select(DeliveryPartner).where(DeliveryPartner.email==email))
       dp = result.scalar()
       if not dp or not pwd_context.verify(password,dp.hashed_password):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password.")
       
       token = jwt.encode(
           payload={
               "delivery_partner":{
                   "id": str(dp.id),
                   "name": dp.name
               },
               "jti": str(uuid4()),
               "exp": datetime.now(timezone.utc)+ timedelta(days=1)
           },
           key=sec.SECRET_KEY, algorithm=sec.ALGORITHM
        )
       return {"access_token": token, "type":"jwt"}