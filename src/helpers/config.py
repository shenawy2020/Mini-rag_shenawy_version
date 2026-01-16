from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION:  str
     
    
    FILE_MAX_SIZE:int
    FILE_ALLOWED_TYPES:list
    FILE_DEFAULT_CHUNK_SIZE: int
    MONOGDB_ULR:str
    MONOGDB_Database:str
    FILE_ALLOWED_EXT:list[str]
    GENERATION_BACKEND : str 

    EMBEDDING_BACKEND: str 

    OPENAI_API_KEY:str=None
    OPENAI_API_URL:str=None

    COHERE_API_KEY:str=None

    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBEDDING_MODEL_SIZE:int=None

    INPUT_DAFAULT_MAX_CHARACTERS:int=None
    GENERATION_DAFAULT_MAX_TOKENS:int=None
    GENERATION_DAFAULT_TEMPERATURE:float  =None
      


   

    class config:
       env_file = ".env"
       SettingsConfigDict
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


def get_settings():
   return Settings()