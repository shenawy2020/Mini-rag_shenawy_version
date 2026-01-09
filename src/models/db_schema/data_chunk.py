from pydantic import BaseModel,Field,validator
from  typing import Optional
from bson.objectid import ObjectId

class Data_chunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text:str =Field(...,min_length=1)
    check_metdadata:dict
    chunk_order: int =Field(...,gt=0)
    chunk_project_id:ObjectId

    class Config:
        arbitrary_types_allowed = True
        populate_by_name=True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}