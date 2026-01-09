from .BaseDataModels import BaseDataModesl
from .db_schema import Data_chunk
from .enums.DatabaseEnum import   DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModesl):
    def __init__(self, dbclient):
        super().__init__(dbclient=dbclient)
        self.Collections=self.dbclient[DataBaseEnum.collection_chunk_name]

    async def create_chunk(self,chunk:Data_chunk):
        result=await self.Collections.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk._id=result.inserted_id        
        return chunk
    
    async def get_chunk(self,chunk_id:str):
        result=await  self.Collections.find_one({
            "_id":ObjectId(chunk_id)
        })
        if result:
            return Data_chunk(**result)
        return None
    async def create_multiple_chunks(self,chunks:list[Data_chunk]):
        operations=[]
        for chunk in chunks:
            operations.append(InsertOne(chunk.dict(by_alias=True, exclude_unset=True)))
        result=await self.Collections.bulk_write(operations)
        return result.inserted_ids
    
    async def create_multiple_chunks_bsize(self,chunks:list[Data_chunk],batch_size:int=100):
        operations=[]
        inserted_ids=[]
        for index,chunk in enumerate(chunks):
            operations.append(InsertOne(chunk.dict(by_alias=True, exclude_unset=True)))
            if (index + 1) % batch_size == 0:
                result=await self.Collections.bulk_write(operations)
                inserted_ids.extend(result.inserted_ids)
                operations=[]
        if operations:
            result=await self.Collections.bulk_write(operations)
            inserted_ids.extend(result.inserted_ids)
        return inserted_ids
    
    async def create_multiple_chunks_bsize_v2(self,chunks:list[Data_chunk],batch_size:int=100):
        for index in range(0,len(chunks),batch_size):
            batch_chunks=chunks[index:index+batch_size]
            operations=[]
            for chunk in batch_chunks:
                operations.append(InsertOne(chunk.dict(by_alias=True, exclude_unset=True)))
            result=await self.Collections.bulk_write(operations)
        return len(chunks)
    
    async def create_multiple_chunks_bsize_v3(self,chunks:list[Data_chunk],batch_size:int=100):
        for index in range(0,len(chunks),batch_size):
            batch_chunks=chunks[index:index+batch_size]
            operations=[
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True  )) for chunk in batch_chunks
            ]
        result=await self.Collections.bulk_write(operations)
        
        return len(chunks)
    
    async def delete_project_chunks(self,project_id:str):
        result=await self.Collections.delete_many({
            "chunk_project_id":ObjectId(project_id)
        })
        return result.deleted_count
    
    

        
    

    
    async def get_chunks_by_project(self,project_id:str):
        chunks=[]
        cursor=self.Collections.find({
            "chunk_project_id":ObjectId(project_id)
        })
        async for document in cursor:
            chunks.append(Data_chunk(**document))
        return chunks   