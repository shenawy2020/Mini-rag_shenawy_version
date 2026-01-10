from .BaseDataModels import BaseDataModesl
from .db_schema import Asset
from .enums.DatabaseEnum import   DataBaseEnum
from bson.objectid import ObjectId


class AssetModel(BaseDataModesl):
    def __init__(self, dbclient):
        super().__init__(dbclient=dbclient)
        self.Collections=self.dbclient[DataBaseEnum.collection_asset_name]
    
    @classmethod
    async def create_instance(cls, dbclient):
        instance = cls(dbclient)
        await instance.init_collections()
        return instance
    
    async def init_collections(self):
        all_collctions=await self.dbclient.list_collection_names()
        if DataBaseEnum.collection_asset_name not in all_collctions:
            self.Collections=self.dbclient[DataBaseEnum.collection_asset_name]
            indexes=Asset.get_indexes()
            for index in indexes :
                await self.Collections.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"] 
                           )   
    async def create_asset(self,asset:Asset):
        result=await self.Collections.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id=result.inserted_id
        return asset
    
    async def get_project_assets(self,asset_project_id:str,asset_type:str):
        searcurecords= await self.Collections.find({ 
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
            ,"asset_type":asset_type
        }).to_list(length=None)
        return [
            Asset(**record)     
         for record in searcurecords
        ]
    async def get_project_assets_byname(self,asset_project_id:str,asset_name:str):
        searcurecords= await self.Collections.find_one({ 
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
            ,"asset_name":asset_name
        }) 
        if searcurecords is None:
            return None
        return   Asset(**searcurecords)     
         
    
    
    

             
    
    async def get_project_assetsV2(self,asset_project_id:str,asset_type:str):
        assets=[]
        cursor= self.Collections.find({ 
            "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
             ,"asset_type":asset_type
        })
        async for document in cursor:
            assets.append(Asset(**document))
        return assets   

