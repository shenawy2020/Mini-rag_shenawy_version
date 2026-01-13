from pydantic import BaseModel,Field,validator
from  typing import Optional

from bson.objectid import ObjectId




class Project(BaseModel):
    #_id:Optional[ObjectId]
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    #id: ObjectId | None = Field(default=None, alias="_id")
    project_id:str =Field(..., min_length=1)
    @validator("project_id")
    def validators_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project id must be alphanumric")\
            
        return value

    class Config:
        arbitrary_types_allowed = True
        populate_by_name=True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
      
    @classmethod
    def get_indexes(cls):
        return [{"key":[("project_id",1)],
                 "name":"project_id_idx",
                 "unique":True}]
    
    # - asc 1 desc -1
    