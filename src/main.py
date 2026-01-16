from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm import LLMProviderFactory


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settting=get_settings()
   # print (settting.MONOGDB_ULR)
    #print (settting.MONOGDB_Database)
    app.mogon_conn= AsyncIOMotorClient(settting.MONOGDB_ULR)
    app.dbclient=app.mogon_conn[settting.MONOGDB_Database]
    #Initialize LLM Provider Factory
    app.Genration_client=LLMProviderFactory(conifig=settting).create_llm_provider(provider=settting.GENERATION_BACKEND)
    app.embedding_client=LLMProviderFactory(conifig=settting).create_llm_provider(provider=settting.EMBEDDING_BACKEND)
    app.Genration_client.set_generatuion_model(mode_id=settting.GENERATION_MODEL_ID)
    #app.Genration_client.set_embedding_model(model_id=settting.EMBEDDING_MODEL_ID,embedding_size=settting.EMBEDDING_MODEL_SIZE) 


@app.on_event("shutdown")
async def shutdown_db_client():
      app.dbclient.close()


#app.rooter.lifespnan.on_startup.append(startup_db_client)   

#app.rooter.lifespnan.on_shutdown.append(shutdown_db_client)


app.include_router(base.base_router)

app.include_router(data.data_router)
