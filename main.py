
from fastapi import FastAPI, HTTPException,status
from contextlib import asynccontextmanager
from rich import print,panel
from scalar_fastapi import get_scalar_api_reference

from session import create_datebase
from router import shipment


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print(panel.Panel('sever is started...',border_style='green'))
    await create_datebase()
    yield 
    print(panel.Panel('server stopped!',border_style='red'))

app = FastAPI(lifespan=lifespan_handler)

# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

app.include_router(shipment.router)

