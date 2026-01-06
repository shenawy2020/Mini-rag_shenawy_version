from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settting=get_settings()
    app.mogon_conn= AsyncIOMotorClient(settting.MONOGDB_ULR)
    app.dbclient=app.mogon_conn(settting.MONOGDB_Database)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.dbclient.close()



app.include_router(base.base_router)

app.include_router(data.data_router)
