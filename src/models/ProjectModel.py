from .BaseDataModels import BaseDataModesl
from .db_schema import Project
from .enums.DatabaseEnum import   DataBaseEnum


class ProjectModel(BaseDataModesl):
    def __init__(self, dbclient):
        super().__init__(dbclient=dbclient)
        self.Collections=self.dbclient[DataBaseEnum.collection_project_name]
       # print("inti Done")
    @classmethod
    async def create_instance(cls, dbclient):
        instance = cls(dbclient)
        await instance.init_collections()
        return instance

    async def init_collections(self):
        all_collctions=await self.dbclient.list_collection_names()
        if DataBaseEnum.collection_project_name not in all_collctions:
            self.Collections=self.dbclient[DataBaseEnum.collection_project_name]
            indexes=Project.get_indexes()
            for index in indexes :
                await self.Collections.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"] 
                           )
                

        




    async def create_project(self,project:Project):
        result=await self.Collections.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id=result.inserted_id
       # project.id=str(result.inserted_id)
        return project
    
    

    async def get_project_or_createone(self, project_id:str):
        record=await self.Collections.find_one(
            {
                "project_id":project_id
            }
        )
        if record is None:
            #crearte new project
            project=Project(project_id=project_id)
            project=await  self.create_project(project=project)
            return project
        
        return Project(**record) 
    
    async def get_all_project(self,page:int=1,page_size:int=10):
        total_doumentscounts=await self.Collections.count_documents({})
        total_pages=total_doumentscounts // page_size
        if total_doumentscounts% page_size>0:
            page_size+=1

        cursor = self.Collections.find().skip( (page-1) * page_size ).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )
        return projects,total_pages


