from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from models import SQLModel
from fastapi import Depends
from config import db_settings

sql_url = db_settings.POSTGRES_URL
engine = create_async_engine(sql_url,echo=True)

async def create_datebase():
    async with engine.begin() as connection:
       await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
     async_session = sessionmaker(
       bind=engine,
       class_= AsyncSession,
       expire_on_commit= False,
   )
     async with async_session() as session:
        yield session




# from typing import Annotated
# from sqlalchemy import create_engine
# from models import SQLModel,Session
# from fastapi import Depends

# sql_url = 'sqlite:///sqlite.db'
# engine = create_engine(sql_url,
#                        connect_args={'check_same_thread' : False},echo=True)

# def create_datebase():
#     SQLModel.metadata.create_all(bind=engine)


# def get_session():
#     with Session(bind=engine) as session:
#         yield session


# sesseionDep = Annotated[Session,Depends(get_session)]