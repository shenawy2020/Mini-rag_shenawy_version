from pydantic import BaseModel,Field,validator
from  typing import Optional
from datetime import datetime


from bson.objectid import ObjectId

class Asset(BaseModel):
    #_id:Optional[ObjectId]
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id:ObjectId
    asset_type:str =Field(..., min_length=1)
    asset_name:str =Field(..., min_length=1)
    asset_size:int =Field(...,gt=0)
    asset_config:dict =Field(default=None)
    asset_pushed_at:datetime =Field(default=datetime.utcnow)


    class Config:
        arbitrary_types_allowed = True
        populate_by_name=True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    @classmethod
    def get_indexes(cls):
            return [ {"key":[("asset_project_id",1)],
                 "name":"asset_project_idx",
                 "unique":False},
                 {"key":[("asset_project_id",1),("asset_name",1)],
                 "name":"asset_project_idx_name_idx",
                 "unique":True}                     ]

