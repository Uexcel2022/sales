from pydantic import EmailStr
from sqlalchemy import INTEGER
from sqlmodel import ARRAY, Column, Relationship, SQLModel,Field,Session
from enum import Enum
from datetime import datetime
from sqlalchemy.dialects import postgresql
from uuid import uuid4,UUID

class ShipmentStatus(str, Enum):
    placed="placed"
    in_transit = "in_transit"
    out_for_delivery= "out_for_delivery"
    delivered="delivered"

class UserBase(SQLModel):
    name: str = Field(regex="^[a-zA-Z]* ?[a-zA-Z]{3,15}$")
    email: EmailStr=Field(unique= True)
    hashed_password:str
    address: int


class Shipment(SQLModel,table=True):
    __tablename__ ='shipment'
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default= uuid4,
            primary_key= True,
          )
        )
    content: str 
    weight: float = Field(..., gt=0, le=25)
    destination: int 
    status: ShipmentStatus 
    estimated_delivery: datetime
    created_at : datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default=datetime.now
            )
        )

    seller_id:UUID = Field(foreign_key="seller.id")
    seller: "Seller"= Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"}
        )
    
    delivery_partner_id:UUID = Field(foreign_key="delivery_partner.id")

    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

   
    

class Seller(UserBase,table=True):
    __tablename__ ="seller"
    id: UUID = Field(
        sa_column= Column(
            postgresql.UUID,
            default= uuid4,
            primary_key=True
        ))
    created_at : datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"}
        )

    def model_dump(self):
        return {
            "id":self.id,
            "name":self.name,
            "email": self.email
        }
    

class DeliveryPartner(UserBase,table=True):
    __tablename__= "delivery_partner"
    id: UUID = Field(
        sa_column= Column(
            postgresql.UUID,
            default= uuid4,
            primary_key=True
        ))
    servicable_zipcode: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER))
    )
    max_handling_capacity : int

    created_at : datetime = Field(
        sa_column= Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def model_dump(self):
        return {
            "id":self.id,
            "name":self.name,
            "email": self.email,
            "servicable_zipcode": self.servicable_zipcode,
            "max_handling_capacity":self.max_handling_capacity

        }
   